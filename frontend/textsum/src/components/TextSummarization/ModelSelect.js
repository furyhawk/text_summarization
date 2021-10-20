import { useEffect, useState } from "react";

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function ModelSelect({ model, setModel }) {
    const [models] = useState(["TDIF", "Transformer"]);

    useEffect(() => {
        setModel(models[1]);
    }, [models, setModel]);

    function handleSelect(e) {
        setModel(e.target.value);
    }

    return (
        <div>
            <FormControl sx={{ m: 1, minWidth: 120 }}>
                <InputLabel id="demo-simple-select-helper-label">Model</InputLabel>
                <Select
                    labelId="demo-simple-select-helper-label"
                    id="demo-simple-select-helper"
                    autoWidth
                    value={model}
                    label="Model"
                    onChange={handleSelect}
                >
                    {models.map(u => (
                        <MenuItem value={u}>{u}</MenuItem>
                    ))}
                </Select>
                <FormHelperText>Select model to use</FormHelperText>
            </FormControl>
        </div>
    );
}