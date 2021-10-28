#!/usr/bin/python3
# --- Librerias
# import datetime
import helper
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from connectDB import DataBase
from enterpriseView import enterpriseView


# -|-|-|-|-|-| Página de inicio |-|-|-|-|-|-
class landingPage:

    def __init__(self, window):
        self.textFont = ('Calibri', 13)

        # ------ Configuraciones de la ventana
        self.wind = window
        self.wind.title('Página Inicial • IDEAR')
        self.wind.call('wm', 'iconphoto', self.wind._w,
                       tk.PhotoImage(file='./Logo2.gif'))

        ancho_ventana = 800
        alto_ventana = 400
        x_ventana = self.wind.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.wind.winfo_screenheight() // 2 - alto_ventana // 2
        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" \
            + str(x_ventana) + "+" + str(y_ventana)

        self.wind.geometry(posicion)
        self.wind.resizable(False, False)
        self.wind.columnconfigure(0, weight=1)
        self.wind.rowconfigure(0, weight=1)

        main_frame = tk.Frame(self.wind, bg="azure").grid(column=0, row=0,
                                                          sticky="nwes")

        # ------ Header widgets ------
        encabezado = tk.Frame(main_frame,
                              borderwidth=2,
                              relief="sunken",
                              padx=25, pady=12,
                              bg="coral")

        # Pega el encabezado a la esquina de la pantalla
        encabezado.grid(row=0, column=0, padx=0, pady=0, sticky="nw")

        self.logoIDEAR = tk.PhotoImage(file="./Logo2.gif").subsample(8)
        tk.Label(encabezado,
                 image=self.logoIDEAR).grid(row=0, column=0,
                                            padx=(15, 560))

        tk.Label(encabezado,
                 text="IDEAR",
                 bg="LightBlue",
                 font=('TkHeadingFont', 20)).grid(row=0, column=2,
                                                  padx=(0, 25))

        # ------ Content ------
        content = tk.Frame(main_frame, bg="azure")
        content.grid(row=0, column=0, padx=25, pady=(75, 10))

        # ------ Verify column ------
        self.verifyFrame = tk.Frame(content,
                                    borderwidth=2,
                                    relief="sunken",
                                    padx=3, pady=12,
                                    bg="pale turquoise")

        self.verifyFrame.grid(row=2, column=1)

        tk.Label(self.verifyFrame,
                 text='Verificar Vacunación',
                 font=('Calibri', 18),
                 bg="pale turquoise").grid(row=0, column=0,
                                           pady=(10, 15))

        tk.Label(self.verifyFrame,
                 text='*Tipo de Documento:',
                 font=self.textFont,
                 bg="pale turquoise").grid(row=1, column=0)

        # Tipo de documento
        tIdentificacion = tk.StringVar()
        tIdentificacion.set('Cédula de Ciudadania')
        self.tipoIdentificacion = ttk.Combobox(self.verifyFrame,
                                               state='readonly',
                                               textvariable=tIdentificacion,
                                               values=('Cédula de Ciudadania',
                                                       'Tarjeta de Identidad',
                                                       'Documento Migratorio')
                                               )
        self.tipoIdentificacion.grid(row=2, column=0, pady=(0, 25))
        # Número de documento
        tk.Label(self.verifyFrame,
                 text='*Número del documento de identificación:',
                 font=self.textFont,
                 bg="pale turquoise").grid(row=3, column=0)

        nIdentificacion = tk.StringVar()
        tk.Entry(self.verifyFrame,
                 textvariable=nIdentificacion).grid(row=4, column=0,
                                                    pady=(0, 25))

        # --- Error valores vacios !
        self.emptyEntryVerify = tk.Label(self.verifyFrame,
                                         text="Por favor ingrese los campos \
                                         requeridos",
                                         bg='red')

        self.emptyEntryVerify.grid_remove()

        # Botón de envio
        tk.Button(self.verifyFrame,
                  bg="moccasin",
                  text='Verificar',
                  command=lambda: self.checking(tIdentificacion,
                                                nIdentificacion)).grid(row=5,
                                                                       column=0
                                                                       )

        # ------ Login as enterprise ------
        self.loginEnterprise = tk.Frame(content,
                                        borderwidth=2,
                                        relief='sunken',
                                        padx=3, pady=12,
                                        bg="pale turquoise")

        self.loginEnterprise.grid(row=2, column=3, padx=(100, 0))

        tk.Label(self.loginEnterprise,
                 text='Acceder como centro médico',
                 font=('Calibri', 18),
                 bg="pale turquoise").grid(row=0, column=0,
                                           pady=(10, 15))

        # --- Número de serie empresa
        tk.Label(self.loginEnterprise,
                 text='*Número de serie:',
                 font=self.textFont,
                 bg="pale turquoise").grid(row=1, column=0)

        nSerieEmpresa = tk.StringVar()
        tk.Entry(self.loginEnterprise,
                 textvariable=nSerieEmpresa).grid(row=2, column=0,
                                                  pady=(0, 25))

        # --- Código de acceso
        tk.Label(self.loginEnterprise,
                 text='*Código de acceso:',
                 font=self.textFont,
                 bg="pale turquoise").grid(row=3, column=0)

        cAcceso = tk.StringVar()
        tk.Entry(self.loginEnterprise,
                 show='•',
                 textvariable=cAcceso).grid(row=4, column=0,
                                            pady=(0, 25))

        # Error valores vacios !
        self.emptyEntryLogin = tk.Label(self.loginEnterprise,
                                        text="Por favor ingrese los campos \
                                        requeridos",
                                        bg='red')

        self.emptyEntryLogin.grid_remove()

        tk.Button(self.loginEnterprise,
                  bg="moccasin",
                  text='Acceder',
                  command=lambda: self.loginAsEnterprise(nSerieEmpresa.get(),
                                                         cAcceso.get())
                  ).grid(row=5,
                         column=0,
                         columnspan=2)

        try:
            self.dbConection = DataBase()
        except Exception as ex:
            numError = ex.args[0]
            messagebox.showerror(
                message="Ocurrio un problema al conectarse a la base de datos",
                title="Error {error} de seridor".format(error=numError)
            )
            self.wind.destroy()
            pass

        # --- MAIN LOOP landing page ------
        self.wind.mainloop()

    # ------ F. verificar un usuario ------
    def checking(self, tIdentificacion, nIdentificacion):

        if not tIdentificacion or not nIdentificacion:
            self.emptyEntryVerify.grid(row=6, column=0,
                                       pady=(10, 15))
            return

        self.emptyEntryVerify.grid_remove()

        # Eliminar el print al final
        print("Checked " + str(nIdentificacion) + str(tIdentificacion))
        return

    # ------ F. Acceder al panel de control ------
    def loginAsEnterprise(self, nSerieEmpresa, cAccesoEmpresa):

        if not nSerieEmpresa or not cAccesoEmpresa:
            self.emptyEntryLogin.grid(row=6, column=0,
                                      pady=(10, 15))
            return

        self.emptyEntryLogin.grid_remove()

        # Esta F. devuelve una tupla, el primer ele. es bool, y el segundo str
        nSerie = helper.clearString(nSerieEmpresa)
        cAcceso = helper.clearString(cAccesoEmpresa)

        if cAcceso[0] or nSerie[0]:
            messagebox.showwarning(message='No se permite el uso de caracteres\
                                   especiales.',
                                   title="Uso de caracteres especiales")
            return
        else:

            respuesta = self.dbConection.verifyEnterprise(nSerie[1],
                                                          cAcceso[1])
            if respuesta:
                # Elimina la ventana de incio "Landing Page"
                self.wind.destroy()
                closeDb = self.dbConection.closeCursor()

                if closeDb:
                    # Abre la ventana del panel de control de la empresa
                    enterpriseView(respuesta)

        return


if __name__ == '__main__':
    window = tk.Tk()
    aplication = landingPage(window)
    # window.mainloop()
