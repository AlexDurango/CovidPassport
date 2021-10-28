import pymysql

class DataBase:

    def __init__(self):

        # -|-|-| Concexion a la base de datos |-|-|-
        self.connect = pymysql.connect(
            host="bsnkengz8ehw6ykbljhc-mysql.services.clever-cloud.com",
            user="uiffd6wbnz2vupwg",
            password="212Po8BG44Yg9y77pyJV",
            db="bsnkengz8ehw6ykbljhc"
        )

        # --- Crear el cursor
        self.cursor = self.connect.cursor()
        print("DB connected")

    # --- Cerrar el cursor abierto
    def closeCursor(self):
        try:
            self.cursor.close()
            return True
        except:
            return False

    # --- Query
    def selectFromTable(self):
        try:
            
            # Hacer Query
            self.cursor.execute("SELECT * FROM usuarios")

            # Terminar la query
            self.connect.commit()

            # Pasar la respuesta a una Tupla
            respond = self.cursor.fetchall()
            if respond:
                return respond
            return False
        except:
            return False

    # --- Query
    def verifyEnterprise(self, nSerie, cAcceso):
        try:
            self.cursor.execute("SELECT * FROM centrosMedicos WHERE numeroDeSerie = '{A}' AND codigoAcceso = '{B}'".format(A = nSerie, B = cAcceso))
            self.connect.commit()
            respond = self.cursor.fetchall()
            if respond:
              return respond
            return False
        except:
            return False

   # --- Query
    def verifyUser(self, tIdentidad, nIdentidad):
        # ! Falta agregar la verificacion del rostro !
        try:
            self.cursor.execute("SELECT * FROM usuarios WHERE tipoIdentiticacions = '{A}' AND numeroIdentificacion = '{B}'".format(A = tIdentidad, B=nIdentidad))
            self.connect.commit()
            respond = self.cursor.fetchall()
            if respond:
                return respond
            return False
        except:
            return False
