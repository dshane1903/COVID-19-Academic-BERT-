### To start app

For React

```bash
yarn start
```

Create another bash instance for Flask:

```bash
yarn start-api
```

### Files

1. Dashboard.js contains
    - Question.js
    - Answers.js
    - Chart.js
    - listItems.js
    - Example.js
2. browser-qa-api contains the Flask app
    - In package.json, `yarn start-api` basically does `cd browser-qa-api && source venv/bin/activate && flask run --no-debugger`
    - Refer to Example.js on how to connecct.
    - ("start-api": "cd browser-qa-api && source venv/bin/activate && flask run --no-debugger"). Removed source venv/bin/activate for compatibility with running on Windows for testing.
    - query method:
        - `/query/<question>`
        - Takes the provided `question` as an argument and returns top articles using BERT
3. All other files are useless

### Download links:

-   https://drive.google.com/open?id=1-JlhSNZQRsAkw8oBeSQoybrLXY1Ru9Cl
-   https://drive.google.com/open?id=1PnPfxibQGVB4LVQF8PU2Z0BaTi0b6iRY

### Command lines used (Useful?)

npm install @material-ui/core

npm install --save material-ui-icons

yarn add @material-ui/icons

npm install recharts

yarn add material-ui-icons
