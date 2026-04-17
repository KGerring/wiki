import re
import os
import sys
import asyncio
import aiohttp
import logging
import argparse
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import pypandoc
from pypandoc.pandoc_download import download_pandoc
import pywikibot
from pywikibot.site._extensions import EchoMixin
#from utils.regex import wikidata_id_regex, spinachbot_top_regex, spinachbot_bottom_regex

wikidata_id_regex = re.compile('P\d+|Q\d+', re.I)
spinachbot_top_regex = re.compile('\{\{spinachbot top\}\}', re.I)
spinachbot_bottom_regex = re.compile('\{\{spinachbot bottom\}\}', re.I)


# Load environment variables
load_dotenv()

# Set up argument parser
parser = argparse.ArgumentParser(description="SpinachBot - Process Wikidata notifications")
parser.add_argument('--dev', action='store_true', help="Run in development environment")
args = parser.parse_args()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/spinachbot-script.log',
    filemode='a'
)
logger = logging.getLogger()

# Redirect stdout and stderr to the logger
class StreamToLogger(object):
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass

sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)

# Set pywikibot logging level
pywikibot_logger = logging.getLogger("pywikibot")
pywikibot_logger.setLevel(logging.WARNING)

class Config:
    """Configuration class for SpinachBot."""
    SITES: List[pywikibot.Site] = [pywikibot.Site('wikidata', 'wikidata')]
    API_KEY: str = os.getenv('API_KEY', '')
    API_URL: str = "https://spinach.genie.stanford.edu/api"

    def __init__(self, dev_mode: bool):
        self.DEV_MODE = dev_mode
        self.TEMPLATE_DIR = './templates' if dev_mode else '/data/project/spinachbot/spinach-bot/templates'
        logger.info(f"Running in {'development' if dev_mode else 'production'} mode")
        logger.info(f"Using template directory: {self.TEMPLATE_DIR}")

config = Config(dev_mode=args.dev)

# Load templates
def load_template(filename: str) -> str:
    """Load a template file from the configured template directory."""
    with open(os.path.join(config.TEMPLATE_DIR, filename), 'r') as f:
        return f.read()

action_history_template: str = load_template('action_history.template')
thought_template: str = load_template('thought.template')
convo_response_template: str = load_template('convo_response.template')

echo = EchoMixin

# Modify pandoc download function to use logging
def download_pandoc_with_logging(*args, **kwargs):
    logger.info("Downloading pandoc...")
    result = download_pandoc(*args, **kwargs)
    logger.info("Pandoc download completed.")
    return result

pypandoc.pandoc_download.download_pandoc = download_pandoc_with_logging
download_pandoc_with_logging()

def configure_csrf_tokens() -> None:
    """Configure CSRF tokens for all sites."""
    for site in config.SITES:
        site.login()
        site.get_tokens(['csrf'])

def get_unread_notifs() -> Dict[str, List[Any]]:
    """
    Retrieve all unread mention notifications for configured sites.

    Returns:
        Dict[str, List[Any]]: A dictionary of unread notifications keyed by site name.
    """
    all_notifs: Dict[str, List[Any]] = {}
    for site in config.SITES:
        notifs = list(echo.notifications(site, filter='!read'))
        all_notifs[site.sitename] = [n for n in notifs if n.category == 'mention']
    return all_notifs

async def fetch(session: aiohttp.ClientSession, url: str, params: Dict[str, str]) -> Dict[str, Any]:
    """
    Asynchronously fetch data from the API.

    Args:
        session (aiohttp.ClientSession): The aiohttp session.
        url (str): The API endpoint URL.
        params (Dict[str, str]): The query parameters.

    Returns:
        Dict[str, Any]: The JSON response from the API or an error dictionary.
    """
    try:
        headers = {'User-Agent': 'SpinachBot pywikibot script'}
        async with session.get(url, params=params, headers=headers, timeout=300) as response:
            response.raise_for_status()
            return await response.json()
    except Exception as e:
        logger.error(f"API fetch error: {str(e)}")
        return {"error": str(e)}

async def process_request(notif: Any, session: aiohttp.ClientSession) -> bool:
    """
    Process a single notification.

    Args:
        notif (Any): The notification object.
        session (aiohttp.ClientSession): The aiohttp session.

    Returns:
        bool: True if processing was successful, False otherwise.
    """
    try:
        wikitext = notif.page.text
        echo.notifications_mark_read(notif.site, list=notif.event_id)
        
        discussion_starts = [m.end() for m in re.finditer(spinachbot_top_regex, wikitext)]
        discussion_ends = [m.start() for m in re.finditer(spinachbot_bottom_regex, wikitext)]

        for s, e in zip(discussion_starts, discussion_ends):
            discussion = wikitext[s:e].strip()
            
            if discussion.endswith('{{spinachbot response end}}') or not discussion or discussion.lower() in ['[[user:spinachbot]]', '@[[user:spinachbot]]', '[[user:spinachbot|spinachbot]]', '@[[user:spinachbot|spinachbot]]']:
                continue

            params = {'question': discussion, 'api_key': config.API_KEY}
            resp = await fetch(session, url=config.API_URL, params=params)

            if 'error' in resp:
                echo.notifications_mark_read(notif.site, unreadlist=notif.event_id)
                logger.error(f"Error in API response: {resp['error']}")
                return False

            resp = resp[0]

            action_history_page = await create_action_history_page(notif, resp)
            new_text = create_convo_response(wikitext, e, resp, action_history_page)

            notif.page.text = new_text
            notif.page.save('SpinachBot reply to a request from this conversation.', botflag=True)
        return True
    except Exception as e:
        echo.notifications_mark_read(notif.site, unreadlist=notif.event_id)
        logger.error(f"Error processing notification: {str(e)}")
        return False

async def create_action_history_page(notif: Any, resp: Dict[str, Any]) -> str:
    """
    Create an action history page for a processed notification.

    Args:
        notif (Any): The notification object.
        resp (Dict[str, Any]): The API response.

    Returns:
        str: The title of the created action history page.
    """
    action_history = ''
    action_history_page_title = f'User:SpinachBot/{notif.site.sitename}_event_{notif.event_id}'

    for i, step in enumerate(resp['actions']):
        llm_thought = step['thought']
        action = get_action_description(step)
        observation = get_observation_description(step)
        
        thought = thought_template.format(step_num=i+1, thought=llm_thought, action=action, observation=observation)
        action_history += thought + '\n'

    wikitext_response = pypandoc.convert_text(resp['response'], 'mediawiki', format='md')
    
    action_history_page_text = action_history_template.format(
        request=resp['question'],
        agent_response=wikitext_response,
        engine=resp['engine'],
        action_history=action_history
    )
    
    page = pywikibot.Page(pywikibot.Site('meta', 'meta'), action_history_page_title)
    page.text = action_history_page_text
    page.save("Creating SpinachBot trace of reasonings and actions record.")
    
    return page.title()

def get_action_description(step: Dict[str, Any]) -> str:
    """
    Generate a description of the action taken in a step.

    Args:
        step (Dict[str, Any]): The step information.

    Returns:
        str: A description of the action.
    """
    if step['action_name'] == 'search_wikidata':
        match = re.findall(wikidata_id_regex, step["action_argument"])
        return f'Searching Wikidata for {{{{Q|{match[0]}}}}}.' if match else f'Searching Wikidata for {step["action_argument"]}.'
    elif step['action_name'] == 'get_wikidata_entry':
        return f'Getting contents of the Wikidata entry {{{{Q|{step["action_argument"]}}}}}.'
    elif step['action_name'] == 'execute_sparql':
        return f'Querying Wikidata using SparQL:\n{{{{Sparql/en|query={step["action_argument"]}\n}}}}.'
    else:
        return "Stopping."

def get_observation_description(step: Dict[str, Any]) -> str:
    """
    Generate a description of the observation in a step.

    Args:
        step (Dict[str, Any]): The step information.

    Returns:
        str: A description of the observation.
    """
    if step['observation'] is None:
        return 'No observation.'
    elif step['observation'] == "":
        return "Did not find any results."
    else:
        return f'<syntaxhighlight lang="wikitext">\n{step["observation"]}\n</syntaxhighlight>'

def create_convo_response(wikitext: str, insert_point: int, resp: Dict[str, Any], action_history_page: str) -> str:
    """
    Create a conversational response to be inserted into the wiki page.

    Args:
        wikitext (str): The original wiki text.
        insert_point (int): The point at which to insert the response.
        resp (Dict[str, Any]): The API response.
        action_history_page (str): The title of the action history page.

    Returns:
        str: The updated wiki text with the response inserted.
    """
    wikitext_response = pypandoc.convert_text(resp['response'], 'mediawiki', format='md')
    convo_resp = convo_response_template.format(wikitext_response=wikitext_response, action_history_page=action_history_page)
    return wikitext[:insert_point] + convo_resp + wikitext[insert_point:]

async def process_notifications(all_notifs: Dict[str, List[Any]]) -> List[bool]:
    """
    Process all notifications concurrently.

    Args:
        all_notifs (Dict[str, List[Any]]): A dictionary of notifications keyed by site name.

    Returns:
        List[bool]: A list of boolean results indicating success or failure for each notification.
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for s in config.SITES:
            for notif in all_notifs[s.sitename]:
                logger.info(f"Processing notification {notif.event_id} on {notif.page.title()}")
                task = asyncio.create_task(process_request(notif, session))
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results

async def main() -> None:
    """Main function to run the SpinachBot script."""
    logger.info("Starting SpinachBot script")
    configure_csrf_tokens()
    all_notifs = get_unread_notifs()
    results = await process_notifications(all_notifs)
    logger.info(f"Processed {len(results)} notifications. Successes: {sum(results)}, Failures: {len(results) - sum(results)}")
    logger.info("SpinachBot script completed")


if __name__ == "__main__":
    asyncio.run(main())