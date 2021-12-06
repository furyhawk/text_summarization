import { useState } from "react";

import ModelSelect from "./ModelSelect";
import TextInput from "./TextInput";
import TextList from "../TextList/TextList";
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';

export default function TextSummarizationView() {
    const [text, setText] = useState("");
    const [textList, setTextList] = useState([]);
    const [metrics, setMetrics] = useState([]);
    const [model, setModel] = useState("Headline");

    return (
        <Box
            sx={{
                boxShadow: 1, // theme.shadows[1]
                color: 'primary.main', // theme.palette.primary.main
                m: 1, // margin: theme.spacing(1)
                p: {
                    xs: 2, // [theme.breakpoints.up('xs')]: { padding: theme.spacing(1) }
                },
                zIndex: 'tooltip', // theme.zIndex.tooltip
            }}>
            <ModelSelect model={model} setModel={setModel} />
            <TextInput text={text} setText={setText}
             textList={textList}
             setTextList={setTextList} metrics={metrics} 
             setMetrics={setMetrics} model={model} />
            <Divider variant="middle" sx={{ my: 3, mx: 2 }} />
            <TextList textList={textList} metrics={metrics} />
        </Box>
    );
}