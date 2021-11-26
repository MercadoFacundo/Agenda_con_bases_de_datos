from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import sqlite3


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar interfaz de usuario
        uic.loadUi("14-Trabajo_2.ui", self)

        # Conectar a la base de datos
        self.conexion = sqlite3.connect('14-Trabajo_2.db')
        self.cursor = self.conexion.cursor()

        self.flag = True
        self.on_cargar()

        self.nuevo.clicked.connect(self.on_nuevo)
        self.editar.clicked.connect(self.on_editar)
        self.aceptar.clicked.connect(self.on_aceptar)
        self.eliminar.clicked.connect(self.on_eliminar)
        self.cancelar.clicked.connect(self.on_cancelar)

        self.on_reset()
        
    def on_reset(self):
        self.nuevo.setEnabled(True)
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.nombre.setDisabled(True)
        self.apellido.setDisabled(True)
        self.correo.setDisabled(True)
        self.telefono.setDisabled(True)
        self.direccion.setDisabled(True)
        self.fecha.setDisabled(True)
        self.altura.setDisabled(True)
        self.peso.setDisabled(True)

    def on_fin_accion(self):
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        self.nuevo.setEnabled(True)

    def on_nuevo(self):
        self.flag = True
        self.nuevo.setEnabled(False)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.nombre.setDisabled(False)
        self.apellido.setDisabled(False)
        self.correo.setDisabled(False)
        self.telefono.setDisabled(False)
        self.direccion.setDisabled(False)
        self.fecha.setDisabled(False)
        self.altura.setDisabled(False)
        self.peso.setDisabled(False)

    def on_editar1(self):
        self.nuevo.setEnabled(False)
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.nombre.setDisabled(False)
        self.apellido.setDisabled(False)
        self.correo.setDisabled(False)
        self.telefono.setDisabled(False)
        self.direccion.setDisabled(False)
        self.fecha.setDisabled(False)
        self.altura.setDisabled(False)
        self.peso.setDisabled(False)

    def on_editar(self):
        self.flag = False
        self.on_editar1()
        
        ids = self.lista.selectedItems()[0]
        filas = self.cursor.execute("SELECT * FROM contactos WHERE id=" + ids.text()[0])
        for fila in filas:
            print(fila[4])
        self.nombre.setText(fila[1])
        self.apellido.setText(fila[2])
        self.correo.setText(fila[3])
        self.telefono.setText(fila[5])
        self.direccion.setText(str(fila[4]))
        self.fecha.setText(fila[6])
        self.altura.setText(str(fila[7]))
        self.peso.setText(str(fila[8])) 

    def on_actualizar(self):
        
        ids = self.lista.selectedItems()[0]
        nombre = str(self.nombre.text())
        apellido = str(self.apellido.text())
        email = str(self.correo.text())
        tel = str(self.telefono.text())
        dir = str(self.direccion.text())
        fechaNac = str(self.fecha.text())
        altura = (self.altura.text())
        peso = (self.peso.text())

        self.lista.addItem(str(nombre + " " + apellido + " " + email + " " + tel + " " + dir + " " + fechaNac+ " " + altura+ " " + peso ))

        self.nombre.setText(str(""))
        self.apellido.setText(str(""))
        self.correo.setText(str(""))
        self.telefono.setText(str(""))
        self.direccion.setText(str(""))
        self.fecha.setText(str(""))
        self.altura.setText(str(""))
        self.peso.setText(str(""))

        self.cursor.execute("UPDATE contactos SET Nombre='"+nombre+"', Apellido='"+apellido+"', Email='"+email+"', Telefono='"+tel+"', Direccion='"+dir+"' , FechaNac='"+fechaNac+"', Altura='"+altura+"', Peso='"+peso +"' WHERE id="+ids.text()[0]) 
        self.conexion.commit() 
    def on_eliminar(self):
        
        mensaje = QMessageBox()
        mensaje.setWindowTitle('Quitar.')
        mensaje.setIcon(QMessageBox.Question)
        mensaje.setInformativeText('¿Esta seguro de querer quitar la fila?')
        mensaje.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        resultado = mensaje.exec()
        if resultado == QMessageBox.Ok:
            ids = self.lista.selectedItems()[0]
            usuario = self.lista.currentRow()

            self.lista.takeItem(usuario)
            self.cursor.execute("DELETE FROM contactos WHERE id = " + ids.text()[0])
            self.conexion.commit() 
            
        elif resultado == QMessageBox.Cancel:
            print('')
            
    def on_cargar(self):
        self.cursor.execute('select * from contactos')
        contactos = self.cursor.fetchall()
        for usuario in contactos:
            id = str(usuario[0])
            nombre = usuario[1]
            apellido = usuario[2]
            email = usuario[3]
            tel = usuario[4]
            dir = usuario[5]
            fechaNac = str(usuario[6])
            altura = str(usuario[7])
            peso = str(usuario[8])
            #print(peso,altura)
            self.lista.addItem(str(id+"   "+nombre  + "   " + apellido + "   " + email + "   " + tel + "   " + dir + "   " + fechaNac+ "   " + altura+ "   " + peso ))

    def on_aceptar(self):
        print(self.flag)
        if self.flag == True:
            self.on_crear()
            print("paso por crear")
            self.on_reset()
            self.on_recargar_lista()
        elif self.flag == False:
            self.on_actualizar()
            self.on_recargar_lista()
    
    def on_cancelar(self):
            self.on_reset()
            self.nombre.setText(str(""))
            self.apellido.setText(str(""))
            self.correo.setText(str(""))
            self.telefono.setText(str(""))
            self.direccion.setText(str(""))
            self.fecha.setText(str(""))
            self.altura.setText(str(""))
            self.peso.setText(str(""))   
        
    def on_crear(self):
        nombre = str(self.nombre.text())
        apellido = str(self.apellido.text())
        email = str(self.correo.text())
        tel = str(self.telefono.text())
        dir = str(self.direccion.text())
        fechaNac = str(self.fecha.text())
        altura = (self.altura.text())
        peso = (self.peso.text())

        self.lista.addItem(str(nombre  + "   " + apellido + "   " + email + "   " + dir + "   " + tel + "   " + fechaNac+ "   " + altura+ "   " + peso ))

        self.nombre.setText(str(""))
        self.apellido.setText(str(""))
        self.correo.setText(str(""))
        self.telefono.setText(str(""))
        self.direccion.setText(str(""))
        self.fecha.setText(str(""))
        self.altura.setText(str(""))
        self.peso.setText(str(""))

        # Agregar usuario
        self.cursor.execute("insert into contactos (Nombre,Apellido,Email,Direccion,Telefono,FechaNac,Altura,Peso) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(nombre, apellido, email, tel,dir,fechaNac,altura,peso))
        self.conexion.commit()

        # Vaciar y volver a cargar lista
        
    def on_recargar_lista(self):
        self.lista.clear()
        self.on_cargar() 

    def closeEvent(self, event):
        self.conexion.close()


app = QApplication([])

win = MiVentana()
win.show()

app.exec_()