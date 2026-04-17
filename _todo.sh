brew install starship zoxide fzf ripgrep bat eza 

# Add to ~/.bashrc
eval “$(starship init bash)”
eval “$(zoxide init bash)”
source <(fzf —bash)
alias cat=“bat”
alias ls=“eza”


