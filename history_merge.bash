#!/bin/echo "BASH Source Script ONLY"
# vim:ft=bash
#
# history_merge.bash
#
# Merge .bash_history and the in-memory history together, sorting it by
# timestamp, and saving in back in-memory and/or back into the history file.
# This is basically a 'merged write' that allows you to merge and share the
# current in-memory history between multiple terminal sessions, when you are
# ready to share it.
#
# Commands are sorted by their recorded timestamps.  The command order in
# a single timestamped entry is preserved for multi-line commands. File locking
# is used to prevent clashes due to multiple shells exiting simultaniously.
#
# This assumes files has bash timestamps.  That is $HISTTIMEFORMAT is set
# (though if you don't like then you can set it to empty string ''), so as NOT
# to print timestamps in "history" command output.  If it is NOT set, then this
# script will NOT work as the commands in the history file will not have
# separators, and thus will be thought to be a single command!
#
# Includes optional code remove older 'duplicate' commands, and to delete
# commands which are 'too simple', or which may contain sensitive information
# like passwords, on the command line.
#
# Adjust script to suit your needs...
#
# WARNING: Before bash version 5, bash would not read timestamped history
# files containing multi-line command correctly.  The mutliple lines would
# become seperate individual entries.
#
####
#
# These are the history setup I have in my ".bash_profile"
#
#   HISTTIMEFORMAT=''       # Save the timestamp, but don't output it
#   #HISTTIMEFORMAT='%F_%T ' # output the time in 'history' see "ht" alias
#
#   # History Aliases...
#   h()  { history 30; }                          # last few history commands
#   ht() { HISTTIMEFORMAT='%F_%T  ' history 30; } # history with time stamps
#
#   # merge and write history
#   hm() { source ~/bin/history_merge.bash; }
#
#   # Replace in-memory history with saved history
#   hr() { if [[ -n $HISTFILE ]]
#          then  history -c; history -r; echo "history read (replace)";
#          else echo "history is disabled";
#          fi }
#
#   # Just write the in-memory history to its save file
#   hw() { if [[ -n $HISTFILE ]]
#          then  history -w; echo "history write (no merge)";
#          else echo "history is disabled";
#          fi }
#
#   # disable history file save
#   hd() { unset HISTFILE; }
#
# And in my ".bash_logout" I have
#
#   # merge and clean history before exiting
#   hm
#   hd  # already saved, no need to save again
#
####
#
# Anthony Thyssen,   8 October 2020
#

# DO not merge if history save has been disabled for some reason
if [[ -e "$HISTFILE" ]]; then

  # create an exclusive lock on the history file
  exec {history_lock}<"$HISTFILE"
  flock $history_lock #|| {
  #echo >&2 "Skipping history merge -- unable to get file lock (NFS?)"
  #exit 1
  #}

  # Temporary file for processing
  histtmp=$( mktemp "${TMPDIR:-/tmp}/bash_history_merge.XXXXXXXXXX" )

  # Break up history into NUL separate records
  # This makes processing a LOT easier, especially with regards to handling
  # multi-line history commands (such as quoted multi-line string args).
  #
  # This also defines the sources of the history being merged...
  #
  perl -pe '$_ = "\0$_" if /^#\d+/'  "$HISTFILE" <(history -w /dev/stdout) |

  # At this point we could just sort by timestamps, and remove the NULs.
  # HOWEVER: records with same timestamp will have the commands sorted too!
  # WARNING: "sort -u -z" does not work, thus the separate "uniq" command.
  #
  # sort -z | uniq -z | tr -d '\0'

  # Perl history merge..
  #
  # This perl sort, also preserves the order of lines with the same timestamp.
  # While removing lines where the commands (even with different timestamps)
  # are the same.
  #
  # It also optionally cleans out things I do not want saved in my history
  # generally as they are ultra simplistic or cryptograpic commands.
  #
  perl -0 -e '
    while(<>) {   # read it all into memory
      s/\0//;                    # remove end of history entry marker
      next unless length;

      # Split timestamp from command
      # Note commands may be multiple-lines!
      # and we may have multiple commands with the same timestamp
      my ( $time, $command ) = split("\n",$_,2);

      $time =~ s/^#(\d+).*/$1/g; # extract the timestamp (and nothing else)
      $command =~ s/^\s+//;      # ignore spaces at start (first line only)
      $command =~ s/\s+$//m;     # ignore space at end of every line
      next unless length($command); # blank command - ignore

      # Optional Code  -- Remove specific commands from history
      #
      # Remove specific commands from history
      next if $command =~ /^(ls|ll|cd|lpr|lpq|ps|pa)\b/;      # simplistic
      next if $command =~ /^(history|h|h[trwdce])\b/;         # history
      next if $command =~ /^(k[se])\b/;                       # keystore
      next if $command =~ /^@($| )/;                          # messages
      next if $command =~ /^(vlc|mplayer|smplayer|totem|ffmpeg)\b/;  # video
      next if $command =~ /^(animate|geeqie|gimp|xv|xvd)\b/;  # image
      next if $command =~ /^(show|video|movie|fcp|do)_/;      # cmd prefix
      next if $command =~ /^#/;                               # comments
      #
      # Remove commands with these arguments
      next if $command =~ /\.(avi|mov|mp4|mpg|mkv|flv)\b/;    # video file
      next if $command =~ /\.(rar)\b/;                        # archive file
      next if $command =~ / \/(mnt|nas)\//;                   # file mounts
      next if $command =~ /password=/;                        # has a password
      #next if $command =~ /https?:\/\//;                     # URLs
      #
      # Special data mark for remote commands
      next if $command =~ /-----.SoD-----/;

      # Optional Code  -- Remove Duplicate Commands
      #
      # Remove any Duplicate commands found (if timestamp is older)
      # This is recommended when merging two or more history sources.
      #
      if ( $old = $time{$command} ) {
        if ( $time >= $old ) {
          # newer command has an older/equal duplicate - remove it
          @{ $history{$old} } = grep { $_ ne $command } @{ $history{$old} }
        } else {
          # this command is older than command already seen - ignore it
          next;
        }
      }

      push @{ $history{$time} }, $command;  # push line into this timestamp
      $time{$command} = $time;              # where to find duplicate commands
    }

    # Output the merged history in timestamp, then command found, order
    foreach $time ( sort {$a<=>$b} keys %history ) {
      foreach $command ( @{ $history{$time} } ) {
        print "#$time\n";
        print "$command\n";
      }
    }
  '  > "$histtmp"

  # Select one or both of the following actions...

  # OPTIONAL: Replace in-memory history with merged history
  history -c
  history -r "$histtmp"

  # OPTIONAL: Replace current $HISTFILE with merged version
  cp "$histtmp" "$HISTFILE"

  # Explicitly release the lock
  exec {history_lock}<&-

  # Clean-up, shred file if posible
  shred -u "$histtmp" || rm "$histtmp"

  unset histtmp

fi

