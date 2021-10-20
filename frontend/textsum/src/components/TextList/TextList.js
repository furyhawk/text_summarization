import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Stack from '@mui/material/Stack';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Badge from '@mui/material/Badge';
import TextSnippetIcon from '@mui/icons-material/TextSnippet';

export default function TextList({ textList }) {
    return (
        <div>

            <List>
                <Stack direction="row"
                    justifyContent="center"
                    alignItems="center"
                    spacing={2}>
                    
                    <Typography gutterBottom variant="h4" component="div">
                        Summarized List
                    </Typography>
                    <Badge badgeContent={textList.length} color="success">
                        <TextSnippetIcon color="action" />
                    </Badge>

                </Stack>
                {textList.map(b => (
                    <ListItem key={b.id}>
                        <Card variant="outlined">
                            <CardContent>
                                {b.text}
                            </CardContent>
                        </Card>

                    </ListItem>

                ))}
            </List>
        </div>
    )
}