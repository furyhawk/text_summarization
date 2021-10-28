import { useState } from "react";

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function ModelSelect({ model, setModel }) {
    const [models] = useState(["TFIDF", "Transformer", "T5", "Finetuned", "Headline"]);

    function handleSelect(e) {
        setModel(e.target.value);
    }

    return (
        <div>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
                <InputLabel id="model-select-label">Model</InputLabel>
                <Select
                    labelId="model-select-label"
                    autoWidth
                    value={model}
                    label="Model"
                    onChange={handleSelect}
                >
                    {models.map((u, index) => (
                        <MenuItem key={index} value={u}>{u}</MenuItem>
                    ))}
                </Select>
                <FormHelperText>Select model to use</FormHelperText>
            </FormControl>
        </div>
    );
}