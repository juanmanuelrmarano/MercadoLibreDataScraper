from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def analizarPagina(marca, modelo, anioDesde, anioHasta):
    anios = {}
    pagina = "https://autos.mercadolibre.com.ar/" + anioDesde + "-" + anioHasta + "/" + marca + "/" + modelo + "/_Desde_0_DisplayType_G"
    driver = webdriver.Chrome("chromedriver")
    driver.get(pagina)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    
    cantResultados = str(soup.find('div',href=False, attrs={'class':'quantity-results'}))
    cantResultados = cantResultados.replace('<div class="quantity-results">','')
    cantResultados = cantResultados.replace(' resultados</div>','')
    cantResultados = cantResultados.replace('.','')
    cantResultados = int(cantResultados)
    
    for x in range(0,cantResultados,48):
        
        pagina = "https://autos.mercadolibre.com.ar/" + anioDesde + "-" + anioHasta + "/" + marca + "/" + modelo + "/_Desde_"+str(x)+"_DisplayType_G"
        driver = webdriver.Chrome("chromedriver")
        driver.get(pagina)

        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        for a in soup.findAll('li',href=False, attrs={'class':'results-item highlighted article grid'}):
            precio = str(a.find('span', attrs={'class':'price__fraction'}))    
            precio = precio.replace('<span class="price__fraction">','')
            precio = precio.replace('</span>','')
            precio = precio.replace('.','')
            precio = int(precio)
            
            kmYAnio = str(a.find('div', attrs={'class':'item__attrs'}))
            print(precio, "   ",kmYAnio[26:30])
            if kmYAnio[26:30] not in anios:
                anios[kmYAnio[26:30]] = precio
                anios[kmYAnio[26:30]+"cant"] = 1
            else:
                anios[kmYAnio[26:30]] = anios[kmYAnio[26:30]] + precio
                anios[kmYAnio[26:30]+"cant"] = anios[kmYAnio[26:30]+"cant"] + 1
        
        for a in soup.findAll('li',href=False, attrs={'class':'results-item highlighted article grid product item-with-attributes'}):
            precio = a.find('span', attrs={'class':'price__fraction'})    
            precio = str(precio)
            precio = precio.replace('<span class="price__fraction">','')
            precio = precio.replace('</span>','')
            precio = precio.replace('.','')
            precio = int(precio)
            
            kmYAnio = a.find('div', attrs={'class':'item__attrs'})
            kmYAnio = str(kmYAnio)
            print(precio, "   ",kmYAnio[26:30])
            if kmYAnio[26:30] not in anios:
                anios[kmYAnio[26:30]] = precio
                anios[kmYAnio[26:30]+"cant"] = 1
            else:
                anios[kmYAnio[26:30]] = anios[kmYAnio[26:30]] + precio
                anios[kmYAnio[26:30]+"cant"] = anios[kmYAnio[26:30]+"cant"] + 1
    print(anios)
    return anios

def calcularPromedios(autos,anioDesde,anioHasta):
    promedios = {}
    for x in range(int(anioDesde), int(anioHasta)+1):
        if str(x) in autos:
            promedios[str(x)] = int(autos[str(x)] / autos[str(x)+"cant"])
    return promedios

def calcularTamaniosGrafico(autos,anioDesde,anioHasta):
    cantTotalAutos = 0
    sizes = []
    for x in range(int(anioDesde), int(anioHasta)+1):
        if str(x) in autos:
            cantTotalAutos = cantTotalAutos + autos[str(x)+"cant"]
            
    for x in range(int(anioDesde), int(anioHasta)+1):
        if str(x) in autos:
            sizes.append((autos[str(x)+"cant"] * 100)/cantTotalAutos)
    return sizes

def definirLabels(autos,preciosPromedioPorAnio,anioDesde,anioHasta):
    labels = []
    for x in range(int(anioDesde), int(anioHasta)+1):
        if str(x) in autos:
            labels.append(str(x) + ": $" + str(preciosPromedioPorAnio[str(x)]))
    return labels
            
def dibujarGrafico(tamanios,labels,marca,modelo,anioDesde,anioHasta):
    fig1, ax1 = plt.subplots()
    ax1.pie(tamanios, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
    ax1.axis('equal')
    fig1.canvas.set_window_title(marca + " " + modelo + " -> " + anioDesde + "-" + anioHasta)
    plt.show()
            
def main():
    marca = input("Escriba la marca del auto a buscar -> ")
    modelo = input("Escriba el modelo del auto a buscar -> ")
    anioDesde = input("Escriba el año inicial de la busqueda -> ")
    anioHasta = input("Escriba el año final de la busqueda -> ")
    autos = {}
    preciosPromedioPorAnio = {}
    autos = analizarPagina(marca,modelo,anioDesde,anioHasta)
    
    preciosPromedioPorAnio = calcularPromedios(autos,anioDesde,anioHasta)
    print(preciosPromedioPorAnio)

    labels = definirLabels(autos,preciosPromedioPorAnio,anioDesde,anioHasta)
    print(labels)

    tamanios = calcularTamaniosGrafico(autos,anioDesde,anioHasta)
    print(tamanios)
    
    dibujarGrafico(tamanios,labels,marca,modelo,anioDesde,anioHasta)
main()
    
