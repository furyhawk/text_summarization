import { useState } from "react";

import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress';


export default function TextInput({ text, setText, textList, setTextList, metrics, setmetrics, model }) {

    const [textRef, setTextRef] = useState("");
    const [busy, setBusy] = useState(false);

    function handleChange(event) {
        setText(event.target.value);
        setTextRef(event.target.value);
    }
    function handleRefChange(event) {
        setTextRef(event.target.value);
    }

    function submit(event) {

        let url = "http://localhost:8000/prediction";

        event.preventDefault();

        setBusy(true);

        fetch(url, {

            method: 'POST',

            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "Access-Control-Allow-Origin": "*"
            },

            body: JSON.stringify({ text: text, reference: textRef, modelId: model })

        }).then((result) => {
            setBusy(false);

            result.json().then((res) => {
                setTextList(textList.concat({ "id": Math.random().toString(36).substr(2, 9), "text": model + " summarized: " + res.summarized + "\n" + res.metrics }));
                setmetrics(res.metrics);
            })

        })
    }

    return (
        <Box
            component="form"
            sx={{
                '& .MuiTextField-root': { m: 1, width: '100ch' },
            }}
            noValidate
            autoComplete="off">
            <div>
                <Stack
                    direction="column"
                    >
                    <Stack
                        direction="row"
                        justifyContent="flex-start"
                        alignItems="flex-start"
                        spacing={{ xs: 1, sm: 2, md: 4 }}>
                        <TextField
                            label="Raw text (x)"
                            multiline
                            value={text}
                            placeholder="Input text summary."
                            onChange={handleChange} disabled={busy} minLength={30}
                            required={true} resize="none" />
                        {busy ?
                            (<CircularProgress />) : (<Button type="submit" onClick={submit}
                                variant="contained" endIcon={<SendIcon />}
                                size="large" ><span>Summarize</span></Button>)}
                    </Stack>
                    <TextField
                        label="Reference summary (y)"
                        value={textRef}
                        placeholder="Input reference summary."
                        onChange={handleRefChange}
                        multiline
                        maxRows={3}
                        disabled={busy} />
                </Stack>
            </div>
        </Box >
    );
}