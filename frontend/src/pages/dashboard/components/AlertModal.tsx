import {
  DialogActionTrigger,
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@chakra-ui/react/button";
import { AlertProps } from "@/pages/dashboard/Types";

const AlertModal: React.FC<AlertProps> = ({
  open,
  setOpen,
  deleteFunction,
}) => {
  return (
    <DialogRoot
      role="alertdialog"
      lazyMount
      open={open}
      onOpenChange={(e) => setOpen(e.open)}
    >
      <DialogContent className="light">
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
        </DialogHeader>
        <DialogBody>
          <p>
            This action cannot be undone. It will permanently delete the
            selected items from MADR.
          </p>
        </DialogBody>
        <DialogFooter>
          <DialogActionTrigger asChild>
            <Button variant="subtle">Cancel</Button>
          </DialogActionTrigger>
          <Button colorPalette="red" onClick={() => deleteFunction()}>
            Delete
          </Button>
        </DialogFooter>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  );
};

export default AlertModal;
