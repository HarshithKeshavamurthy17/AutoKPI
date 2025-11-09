#!/bin/bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
\n\
[theme]\n\
primaryColor = '#8b5cf6'\n\
backgroundColor = '#000000'\n\
secondaryBackgroundColor = '#1a1a1a'\n\
textColor = '#e5e7eb'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml

