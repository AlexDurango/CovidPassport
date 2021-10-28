# --- Librerias
# import datetime
# import helper
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from connectDB import DataBase


# -|-|-|-|-| Panel de control empresa |-|-|-|-|-|-
class enterpriseView:

    def __init__(self, infoCenMed):

        # Info query centro medico
        self.infoCM = {'index': infoCenMed[0][0],
                       'Nombre': infoCenMed[0][1],
                       'Numero Serie': infoCenMed[0][2],
                       'Ciudad': infoCenMed[0][4],
                       'Fecha Union': infoCenMed[0][6].strftime('%B %d, %Y')}

        # ------ Configuración ventana
        self.enterpriseWindow = tk.Tk()
        self.enterpriseWindow.title('Panel de control • '
                                    + self.infoCM['Nombre'])
        self.enterpriseWindow.call('wm',
                                   'iconphoto',
                                   self.enterpriseWindow._w,
                                   tk.PhotoImage(file='./Logo2.gif'))

        # ancho_ventana = 1200
        # alto_ventana = 680
        self.enterpriseWindow.attributes('-zoomed', True)

        self.enterpriseWindow.resizable(width=True, height=True)
        self.enterpriseWindow.columnconfigure(0, weight=1)
        self.enterpriseWindow.rowconfigure(0, weight=1)

        mFrameEnterprise = tk.Frame(self.enterpriseWindow,
                                    bg='pink').grid(column=0, row=0,
                                                    sticky='nwes')

        # --- Content Frame
        content = tk.Frame(mFrameEnterprise, bg="pink")
        content.grid(row=0, column=0, padx=25, pady=(25, 0),
                     sticky='nwes')

        # -|-|-|-|-|-| LeftSide Frame |-|-|-|-|-|-|-
        leftSideF = tk.Frame(content, bg='pink')
        leftSideF.grid(row=0, column=0,
                       padx=15, pady=(0, 5),
                       sticky='nw')

        textFrame = tk.Frame(leftSideF, bg='white')
        textFrame.grid(row=0, column=0,
                       padx=15, pady=(0, 5),
                       sticky='we')
        # --- Texto left side

        # Main Title
        tk.Label(textFrame,
                 font=('Calibri', 45),
                 bg='white',
                 foreground='#54aae8',
                 text='Vista General').grid(row=0, column=0,
                                            padx=(175, 0), pady=15,
                                            sticky='we')

        descriptionTextFrame = tk.Frame(textFrame,
                                        bg='lightBlue')
        descriptionTextFrame.grid(row=1, column=0,
                                  padx=(160, 0), pady=(0, 15),
                                  sticky='we')

        tk.Label(descriptionTextFrame,
                 bg='lightBlue',
                 font=('Calibri', 18),
                 text='En la tabla inferior se muestran las personas vacunadas'
                 + ' por'
                 ).grid(row=0, column=0,
                        padx=15, pady=(15, 0),
                        sticky='we')

        tk.Label(descriptionTextFrame,
                 bg='lightBlue',
                 font=('Calibri', 18),
                 text='{name}, {city}.'.format(name=self.infoCM['Nombre'],
                                               city=self.infoCM['Ciudad'])
                 ).grid(row=1, column=0,
                        padx=15, pady=(10, 30),
                        sticky='we')

        tk.Label(descriptionTextFrame,
                 bg='lightBlue',
                 font=('Calibri', 18),
                 text='Los registros verdes son aquellos con inmunidad total,'
                 ).grid(row=2, column=0,
                        padx=0, pady=(0, 5),
                        sticky='we')

        tk.Label(descriptionTextFrame,
                 bg='lightBlue',
                 font=('Calibri', 18),
                 text='mientras que los amarillos tiene inmunidad parcial.'
                 ).grid(row=3, column=0,
                        padx=0, pady=(0, 15),
                        sticky='we')

        tk.Label(descriptionTextFrame,
                 bg='lightBlue',
                 font=('Calibri', 18),
                 text='Para editar un registro, debe seleccionarlo primero.'
                 ).grid(row=4, column=0,
                        padx=0, pady=(15, 15),
                        sticky='we')

        # ------ Barra Busqueda -------
        barraBusqueda = tk.LabelFrame(leftSideF,
                                      borderwidth=4,
                                      relief="sunken",
                                      padx=5, pady=10,
                                      text='Barra de busqueda',
                                      bg='white')

        barraBusqueda.grid(row=1, column=0,
                           padx=15, pady=(25, 20),
                           sticky='nw')

        searchTypeValue = tk.StringVar()
        searchTypeValue.set('Nombre')
        searchType = ttk.Combobox(barraBusqueda,
                                  width=15,
                                  state='readonly',
                                  textvariable=searchTypeValue,
                                  values=('Nombre',
                                          'Tarjeta Identidad',
                                          'Cédula'
                                          )
                                  )
        searchType.grid(row=0, column=0, pady=(5, 5))

        searchValue = tk.StringVar()
        searchValueEntry = tk.Entry(barraBusqueda,
                                    textvariable=searchValue,
                                    width=91)
        searchValueEntry.grid(row=0, column=1, pady=(5, 5))

        searchButton = tk.Button(barraBusqueda,
                                 bg='lightGreen',
                                 text='Buscar',
                                 command=lambda:
                                 self.buscarUser(searchTypeValue,
                                                 searchValue)
                                 )
        searchButton.grid(row=0, column=2, pady=(5, 5))

        # -|-|-|-|-|-| Tabla de usuarios |-|-|-|-|-|-
        self.tableStyle = ttk.Style()
        self.tableStyle.configure("Treeview",
                                  background='silver',
                                  foregorund='black',
                                  rowheight=25,
                                  fieldbackground='lightGreen')

        self.tabla_frame = tk.Frame(leftSideF,
                                    bg='pink')
        self.tabla_frame.grid(row=2, column=0,
                              padx=0, pady=0,
                              sticky='nw')

        self.t_scrollY = tk.Scrollbar(self.tabla_frame)
        self.t_scrollY.grid(row=0, column=1,
                            sticky='ns')

        # --- Hace la query y muestra la tabla en pantalla
        self.showAllUsersTable()

        # --- Configuracion Barra Scroll
        self.t_scrollY.config(command=self.tablaUsuarios.yview,
                              orient='vertical')

        ttk.Separator(content,
                      orient=tk.HORIZONTAL).grid(row=0, column=1,
                                                 sticky='ns')

        # -- Botón para refrescar la tabla

        tk.Button(leftSideF,
                  text='Refrescar tabla',
                  bg='#54aae8',
                  foreground='white',
                  command=self.showAllUsersTable
                  ).grid(row=4, column=0,
                         padx=15, pady=(10, 0),
                         sticky='we')

        # -|-|-|-|-|-| Right Side |-|-|-|-|-|-
        rigthSideF = tk.Frame(content,
                              bg='lightBlue')
        rigthSideF.grid(row=0, column=2,
                        padx=15, pady=15,
                        sticky='ne')

        # --- MAIN LOOP enterprise view
        self.enterpriseWindow.mainloop()

    # --- F. Agregar a la tabla los usuarios

    def showAllUsersTable(self):

        try:
            self.dbConection = DataBase()
            self.usuariosVacunados = self.dbConection.selectFromTable()

        except Exception as ex:
            numError = ex.args[0]
            messagebox.showerror(
                message="Ocurrio un problema al conectarse a la base de datos",
                title="Error {error} de seridor".format(error=numError)
            )
            self.enterpriseWindow.destroy()
            pass

        if hasattr(enterpriseView, 'self.tablaUsuarios'):
            self.tablaUsuarios.destroy()

        self.tablaUsuarios = ttk.Treeview(self.tabla_frame,
                                          style='Treeview',
                                          yscrollcommand=self.t_scrollY.set,
                                          selectmode='browse')

        if self.usuariosVacunados:

            # --- Configura la altura de la tabla a la cantidad de usuarios
            self.tablaUsuarios['height'] = len(self.usuariosVacunados) \
                if len(self.usuariosVacunados) <= 10 else 10

            # ------ Configurando las columnas ------
            self.tablaUsuarios['columns'] = ('Nombre Completo',
                                             'Tipo Documento',
                                             'Num Documento',
                                             'Tipo vacuna',
                                             'Dosis',
                                             'Fecha vacunacion',
                                             'Correo')
            # Elimina la columna 'madre'
            self.tablaUsuarios.column('#0', width=0, stretch=tk.NO)
            # --- Seteando cada columna a mano
            self.tablaUsuarios.column('Nombre Completo',
                                      width=215,
                                      minwidth=150,
                                      anchor='w')
            self.tablaUsuarios.heading('Nombre Completo',
                                       text='Nombre Completo')
            self.tablaUsuarios.column('Tipo Documento',
                                      width=50,
                                      minwidth=25,
                                      anchor=tk.CENTER)
            self.tablaUsuarios.heading('Tipo Documento',
                                       text='Documento')
            self.tablaUsuarios.column('Num Documento',
                                      width=115,
                                      minwidth=50,
                                      anchor=tk.CENTER)
            self.tablaUsuarios.heading('Num Documento',
                                       text='N° Documento')
            self.tablaUsuarios.column('Tipo vacuna',
                                      width=90,
                                      minwidth=50,
                                      anchor=tk.CENTER)
            self.tablaUsuarios.heading('Tipo vacuna', text='Vacuna')
            self.tablaUsuarios.column('Dosis',
                                      width=50,
                                      minwidth=15,
                                      anchor=tk.CENTER)
            self.tablaUsuarios.heading('Dosis',
                                       text='Dosis')
            self.tablaUsuarios.column('Fecha vacunacion',
                                      width=150,
                                      minwidth=100,
                                      anchor=tk.CENTER)
            self.tablaUsuarios.heading('Fecha vacunacion',
                                       text='Fecha Vacunación')
            self.tablaUsuarios.column('Correo',
                                      width=275,
                                      minwidth=200,
                                      anchor=tk.CENTER)
            self.tablaUsuarios.heading('Correo',
                                       text='Correo Electrónico')

            self.dbConection.closeCursor()
        else:

            # En caso de no encontrar usuarios vacunados por esa empresa
            self.tablaUsuarios.column('#0', width=0, stretch=tk.NO)
            # Se pone unicamente una columna con el nombre 'Tabla vacia'
            self.tablaUsuarios['columns'] = ('EmptyTable')
            self.tablaUsuarios['height'] = 2
            self.tablaUsuarios.column('EmptyTable',
                                      width=932, anchor=tk.CENTER)
            self.tablaUsuarios.heading('EmptyTable',
                                       text='No se encontraron usuarios')

            # Modifica el estilo de la tabla para hacer texto mśa grande
            self.tableStyle.configure("Treeview",
                                      font=('Calibri', 20),
                                      background='silver',
                                      foregorund='white',
                                      rowheight=75,
                                      fieldbackground='lightGreen'
                                      )
            self.tablaUsuarios['style'] = 'Treeview'
            self.tablaUsuarios.insert("", tk.END,
                                      values=('Aún no se ha agregado \
                                                  usuarios',),
                                      tags=('emptyRow'))

            self.tablaUsuarios.insert("", tk.END,
                                      values=('Empieza a agregarlos!',),
                                      tags=('emptyRow2'))
            self.tablaUsuarios.tag_configure('emptyRow',
                                             background='Yellow')
            self.tablaUsuarios.tag_configure('emptyRow2',
                                             background='lightGreen')

        # --- Imprimiendo la info de los usuarios
        if self.usuariosVacunados:

            for user in self.usuariosVacunados:
                usuario = {'ID': user[0],
                           'Vacunado Por': user[1],
                           'Nombre': user[2],
                           'TipoDoc': 'TI' if user[3] == 'Tarjeta de Identidad'
                           else 'CC' if user[3] == 'Cédula de Ciudadania'
                           else 'PAS',
                           'NumDoc': user[4],
                           'TipoVac': user[6],
                           'Dosis': user[7],
                           'FechaUnion': user[8].strftime('%B %d, %Y'),
                           'Correo': user[9]}

                self.tablaUsuarios.insert("",
                                          tk.END,
                                          values=(usuario['Nombre'],
                                                  usuario['TipoDoc'],
                                                  usuario['NumDoc'],
                                                  usuario['TipoVac'],
                                                  usuario['Dosis'],
                                                  usuario['FechaUnion'],
                                                  usuario['Correo']
                                                  ),
                                          tags=('dosisI',)
                                          if usuario['Dosis'] == '1'
                                          and usuario['TipoVac'] != 'J&J'
                                          else ('dosisII',)
                                          )

            self.tablaUsuarios.tag_configure('dosisI',
                                             background='yellow')
            self.tablaUsuarios.tag_configure('dosisII',
                                             background='lightGreen')

        # --- Rellena la tabla con la info
        self.tablaUsuarios.grid(row=0, column=0, padx=(15, 0), pady=(0, 0))

        return

    def buscarUser(self, tipoQuery, searchValueE):
        print('Buscando '
              + str(tipoQuery.get())
              + ' al usuario: '
              + str(searchValueE.get()))
        return
