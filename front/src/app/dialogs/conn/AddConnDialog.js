import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  TextField,
  useMediaQuery,
  useTheme,
} from "@mui/material";

export default function AddConnDialog({ open, closeAction, addAction, environments }) {
  // Data for handling forms dialogs and confirmations
  const theme = useTheme();
  const fullscreen = useMediaQuery(theme.breakpoints.down("md"));
  return (
    <Dialog fullscreen={fullscreen} open={open} onClose={closeAction}>
      <DialogTitle>Add Connection</DialogTitle>
      <DialogContent>
        <Box
          component="form"
          sx={{ "& .MuiTextField-root": { m: 1, width: "25ch" } }}
          noValidate
          autoComplete="off"
        >
          <div>
            <TextField id="conn-name" label="Name" />
          </div>
          <div>
            <TextField
              id="conn-desc"
              label="Description"
              multiline
              maxRows={4}
            />
          </div>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={addAction} autoFocus>
          Create
        </Button>
        <Button onClick={closeAction}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
}
