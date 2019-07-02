import mcpras
import excel
sw = True
while sw==True:
    print('Ingrese 1 para ajustar voltaje, 2 para descargar historicos')
    x = input()
    if x==1:
        sw1 = True
        while sw1==True:
              print('Ingrese el valor de voltaje entre el rango de 14.5 y 18.6')
              v = input()
              n = excel.main(float(v),0)
	      n = int(n)
              mcpras.set_value(n)
              print('Para salir ingrese 3, para seguir ajustando 1')
              y = input()
              if y==3:
                 sw1=False
              elif y==1:
                 sw1= True
    if x==2:
        excel.main(0,1)
        print('Descargado')


