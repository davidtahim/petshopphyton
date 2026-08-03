from tkinter import TclError


def main():
    try:
        from app.gui import PetShopApp

        app = PetShopApp()
        app.mainloop()
        return
    except TclError:
        print("Tkinter não está disponível neste ambiente. Abrindo o sistema em terminal...")
        from app.main import main as terminal_main

        terminal_main()


if __name__ == "__main__":
    main()
