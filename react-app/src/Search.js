import React, { useState } from 'react';
import Link from '@material-ui/core/Link';
import Title from './Title';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import CircularProgress from '@material-ui/core/CircularProgress';
import './Search.css';
import Plot from 'react-plotly.js';

function preventDefault(event) {
    event.preventDefault();
}

export default function Search() {
    // Functional Component using States
    // https://stackoverflow.com/questions/46821699/react-functional-component-using-state/53780465

    // Reference for text input
    const input = React.createRef();
    const loading = React.createRef();

    // Default placeholder values
    const [keywords, setKeywords] = useState([]);
    const [scores, setScores] = useState([]);
    const [suggestions, setSuggestions] = useState([
        'What are the symptoms of COVID-19?',
        'The economic effects of a pandemic',
        'Bayesian inference for emerging infectious diseases',
    ]);
    const [answers, setAnswers] = useState([
        {
            id: 0,
            score: 0.687,
            url: 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5028948/',
            title:
                'Cats are not small dogs: is there an immunological explanation for why cats are less affected by arthropod-borne disease than dogs?',
            abstract:
                'It is widely recognized that cats appear to be less frequently affected by arthropod-borne infectious diseases than dogs...',
        },
    ]);

    function handleSubmit(event) {
        if (input.current.value.length === 0) {
            console.log('no input');
            input.current.style.borderColor = 'darkred';
            return;
        }
        input.current.style.borderColor = 'lightgray';
        preventDefault(event); // avoids refreshing page after submit
        updateAnswers(input.current.value);
    }

    function handleClick(event) {
        // Only update answers when u click a button
        if (event.target.value) {
            updateAnswers(event.target.value);
        }
    }

    function updateAnswers(input) {
        const headers = {
            headers: {
                'Content-Type': 'application/json',
                Accept: 'application/json',
            },
        };
        loading.current.style.opacity = 1;
        fetch('/query/' + input, headers)
            .then((response) => {
                return response.json();
            })
            .then((json) => {
                let newAnswers = [];
                // let context = '';
                let context = [];
                let i;
                for (i = 0; i < 5; i++) {
                    let row = {
                        id: i,
                        score: json.answer.score[i],
                        url: json.answer.url[i],
                        title: json.answer.title[i],
                        abstract: json.answer.abstract[i],
                    };
                    newAnswers.push(row);
                    context.push(row.abstract);
                }
                // Update Answers in the tables
                setAnswers(newAnswers);

                // Update suggestions
                setSuggestions(json.suggestions);

                // Update keywords
                setKeywords(json.keywords);
                setScores(json.scores);

                // TODO: Fix this
                // loading.current.style.opacity = 0;
            });
    }

    return (
        <React.Fragment>
            <Title>Search</Title>
            <form id="question-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="What effect does COVID-19 have on pets?"
                    ref={input}
                />
                <div className="btn-wrapper">
                    <Link color="primary" onClick={handleSubmit}>
                        Enter
                    </Link>
                    <div id="loading" ref={loading}>
                        <CircularProgress size="2rem" />
                    </div>
                </div>
            </form>

            <br />
            <br />

            <Title>Answers</Title>
            <Table size="small">
                <TableHead>
                    <TableRow>
                        <TableCell style={{ width: '10%' }}>Score:</TableCell>
                        <TableCell style={{ width: '20%' }}>URL:</TableCell>
                        <TableCell style={{ width: '20%' }}>Title:</TableCell>
                        <TableCell style={{ width: '50%' }}>
                            Abstract:
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {answers.map((row) => (
                        <TableRow key={row.id}>
                            {/* Round up to 5 decimal places */}
                            <TableCell>{row.score.toFixed(5)}</TableCell>
                            <TableCell>{row.url}</TableCell>
                            <TableCell>{row.title}</TableCell>
                            <TableCell>{row.abstract}</TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>

            <br />
            <br />

            <Title>Suggestions</Title>
            {suggestions.map((suggestion) => (
                <div className="btn-suggestion" key={suggestion}>
                    <input
                        type="button"
                        value={suggestion}
                        onClick={(e) => handleClick(e, 'value')}
                    />
                </div>
            ))}

            <br />
            <br />

            <Title>Keywords</Title>
            {/* Center the plot */}
            <div
                style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Plot
                    data={[
                        {
                            type: 'bar',
                            x: keywords,
                            y: scores,
                            marker: { color: 'lightgrey' },
                        },
                    ]}
                    layout={{
                        width: 1024,
                        height: 400,
                        title: 'Word importance',
                        xaxis: {
                            title: 'Tokens',
                        },
                        yaxis: {
                            title: 'Score',
                        },
                    }}
                />
            </div>

            <br />
            <br />
        </React.Fragment>
    );
}
