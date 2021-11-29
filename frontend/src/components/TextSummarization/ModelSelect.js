// import { useState } from "react";
import { useQuery } from "react-query";

import getData from "../../utils/api";

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormHelperText from '@mui/material/FormHelperText';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import CircularProgress from '@mui/material/CircularProgress';

export default function ModelSelect({ model, setModel }) {
    // const [models] = useState(["TFIDF", "Transformer", "T5", "Finetuned", "Headline"]);
    let url = `http://${window.location.hostname}:8000/models`;
    const { data: models = [model] } = useQuery(
        "models",
        () => getData(url),
    );

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
                    {models.model ? (models.model.map((u, index) => (
                        <MenuItem key={index} value={u}>{u}</MenuItem>
                    ))) : (<CircularProgress />)}
                </Select>
                <FormHelperText>Select model to use</FormHelperText>
            </FormControl>
        </div>
    );
}