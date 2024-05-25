import os
import time
import datetime
import pandas as pd
from tqdm import tqdm
import requests
import xml.etree.ElementTree as et


# Como podemos tener miles de referencias o coordenadas que mirar,
# cada x referencias vamos a guardar el output y así no perdemos resultados.
# Definimos el tamaño de los trozos que vamos a crear:
LISTSIZE = 300
SCRIPT_PATH = os.getcwd()
INPUT_PATH = os.path.join(SCRIPT_PATH, 'input')
OUTPUT_PATH = os.path.join(SCRIPT_PATH, 'output')


def api_catastro_referencias_catastrales(list_referencias):
    # Obtenemos la cantidad de referencias:
    total_referencias = len(list_referencias)
    print(f"Cargadas {total_referencias} referencias catastrales.")

    df_output = pd.DataFrame()
    for item in tqdm(list_referencias, desc='Scraping'):
        dict_results = {}
        dict_referencia_unicas = {}

        # Para evitar baneos (en segundos). Tras muchas pruebas, menos de 2 segundos no es posible.
        time.sleep(2)

        # Control sobre la referencia:
        # Si la referencia tiene una ñ nos la saltamos para evitar fallos de la API:
        if item.lower().find("ñ") >= 0:
            # Corregir esto para que la referencia salga pero marcando un error
            continue
        # En el formato al que decodificamos, el espacio viene como "\xa0", los quitamos si hubiera:
        elif item.find("\xa0") >= 0:
            item = item.replace(u'\xa0', u'')

        # Dirección del API OVCCoordenadas/Consulta_CPMRC para la descarga de los datos XML de geolocalización
        url = 'http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/' \
              'Consulta_CPMRC?Provincia=&Municipio=&SRS=EPSG:4326&RC='

        # Obtenemos la referencia catastral matriz (14 caracteres), por ejemplo: 9076901BE4397N
        matriz_catastral = item[0:14:]

        # Crea la url completa con esta matriz:
        url_matriz_completa = url + matriz_catastral

        # Llamamos a la API:
        response = requests.get(url_matriz_completa)

        # Obtenemos el XML:
        root = et.fromstring(response.content)

        # Comprueba que la información es correcta
        control = root.find(".//{http://www.catastro.meh.es/}control")
        control_geo = control.find(".//{http://www.catastro.meh.es/}cucoor").text

        # Captura los datos de la geolocalización:
        coord = root.find(".//{http://www.catastro.meh.es/}coord")
        pc1 = coord.find(".//{http://www.catastro.meh.es/}pc1").text
        pc2 = coord.find(".//{http://www.catastro.meh.es/}pc2").text
        x_cen = coord.find(".//{http://www.catastro.meh.es/}xcen").text
        y_cen = coord.find(".//{http://www.catastro.meh.es/}ycen").text
        srs = coord.find(".//{http://www.catastro.meh.es/}srs").text
        ldt = coord.find(".//{http://www.catastro.meh.es/}ldt").text

        dict_results[item] = {
            'matriz': pc1+pc2,
            'pc1': pc1,
            'pc2': pc2,
            'x_cen': x_cen,
            'y_cen': y_cen,
            'srs': srs,
            'ldt': ldt
        }

        # Cambiamos variable de error:
        error_str = 'NO'

        # API OVCSWLocalizacionRC/OVCCallejero DESCARGA INFORMACIÓN PUBLICA
        # Dirección del API OVCSWLocalizacionRC/OVCCallejero para la descarga
        # de los datos XML de la información pública

        url2 = 'http://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCallejero.asmx/' \
               'Consulta_DNPRC?Provincia=&Municipio=&RC='

        # Crea la url completa y llamamos a la api para obtener el XML:
        url_completa_2 = url2 + item
        response = requests.get(url_completa_2)
        root = et.fromstring(response.content)

        # En función de si tenemos una matriz catastral o una referencia única el XML cambia.
        if len(item) == 14:
            # Si metemos una matriz catastral, podemos obtener, obtendremos tantas etiquetas <rcdnp>
            # como referencias catastrales únicas haya, por tanto, debemos buscarlas todas:
            rcdnp_list = root.findall(".//{http://www.catastro.meh.es/}rcdnp")

            for rcdnp in rcdnp_list:
                car = rcdnp.find(".//{http://www.catastro.meh.es/}car").text
                cc1 = rcdnp.find(".//{http://www.catastro.meh.es/}cc1").text
                cc2 = rcdnp.find(".//{http://www.catastro.meh.es/}cc2").text
                cp = rcdnp.find(".//{http://www.catastro.meh.es/}cp").text
                cm = rcdnp.find(".//{http://www.catastro.meh.es/}cm").text
                cmc = rcdnp.find(".//{http://www.catastro.meh.es/}cmc").text
                np = rcdnp.find(".//{http://www.catastro.meh.es/}np").text
                nm = rcdnp.find(".//{http://www.catastro.meh.es/}nm").text
                cv = rcdnp.find(".//{http://www.catastro.meh.es/}cv").text
                tv = rcdnp.find(".//{http://www.catastro.meh.es/}tv").text
                nv = rcdnp.find(".//{http://www.catastro.meh.es/}nv").text
                pnp = rcdnp.find(".//{http://www.catastro.meh.es/}pnp").text
                plp = rcdnp.find(".//{http://www.catastro.meh.es/}plp").text
                td = rcdnp.find(".//{http://www.catastro.meh.es/}td").text
                es = rcdnp.find(".//{http://www.catastro.meh.es/}es").text
                pt = rcdnp.find(".//{http://www.catastro.meh.es/}pt").text
                pu = rcdnp.find(".//{http://www.catastro.meh.es/}pu").text
                dp = rcdnp.find(".//{http://www.catastro.meh.es/}dp").text
                dm = rcdnp.find(".//{http://www.catastro.meh.es/}dm").text

                referencia_unica = pc1+pc2+car+cc1+cc2
                dict_referencia_unicas[referencia_unica] = {
                    'matriz': pc1+pc2,
                    'car': car,
                    'cc1': cc1,
                    'cc2': cc2,
                    'cp': cp,
                    'cm': cm,
                    'cmc': cmc,
                    'np': np,
                    'nm': nm,
                    'cv': cv,
                    'tv': tv,
                    'nv': nv,
                    'pnp': pnp,
                    'plp': plp,
                    'td': td,
                    'es': es,
                    'pt': pt,
                    'pu': pu,
                    'dp': dp,
                    'dm': dm
                }
            df_referencias_unicas = pd.DataFrame(dict_referencia_unicas).T
        # Si tenemos una referencia de 20 dígitos, vamos directamente a por los valores:
        else:
            df_referencias_unicas = pd.DataFrame()

            bico = root.find(".//{http://www.catastro.meh.es/}bico")
            car = bico.find(".//{http://www.catastro.meh.es/}car").text
            cc1 = bico.find(".//{http://www.catastro.meh.es/}cc1").text
            cc2 = bico.find(".//{http://www.catastro.meh.es/}cc2").text
            cp = bico.find(".//{http://www.catastro.meh.es/}cp").text
            cm = bico.find(".//{http://www.catastro.meh.es/}cm").text
            cmc = bico.find(".//{http://www.catastro.meh.es/}cmc").text
            np = bico.find(".//{http://www.catastro.meh.es/}np").text
            nm = bico.find(".//{http://www.catastro.meh.es/}nm").text
            cv = bico.find(".//{http://www.catastro.meh.es/}cv").text
            tv = bico.find(".//{http://www.catastro.meh.es/}tv").text
            nv = bico.find(".//{http://www.catastro.meh.es/}nv").text
            pnp = bico.find(".//{http://www.catastro.meh.es/}pnp").text
            plp = bico.find(".//{http://www.catastro.meh.es/}plp").text
            td = bico.find(".//{http://www.catastro.meh.es/}td").text
            es = bico.find(".//{http://www.catastro.meh.es/}es").text
            pt = bico.find(".//{http://www.catastro.meh.es/}pt").text
            pu = bico.find(".//{http://www.catastro.meh.es/}pu").text
            dp = bico.find(".//{http://www.catastro.meh.es/}dp").text
            dm = bico.find(".//{http://www.catastro.meh.es/}dm").text

            dict_results[item].update({
                'car': car,
                'cc1': cc1,
                'cc2': cc2,
                'cp': cp,
                'cm': cm,
                'cmc': cmc,
                'np': np,
                'nm': nm,
                'cv': cv,
                'tv': tv,
                'nv': nv,
                'pnp': pnp,
                'plp': plp,
                'td': td,
                'es': es,
                'pt': pt,
                'pu': pu,
                'dp': dp,
                'dm': dm
            })

        df_result = pd.DataFrame(dict_results).T
        df_result.reset_index(inplace=True)

        if len(df_referencias_unicas) > 0:
            df_final = df_result.merge(df_referencias_unicas, on='matriz', how='left')
        else:
            df_final = df_result

        df_final.drop(columns=['matriz'], inplace=True)
        df_final.rename(columns={'index': 'referencia catastral'}, inplace=True)

        column_order = ['referencia catastral',
                        'pc1', 'pc2', 'car', 'cc1', 'cc2',
                        'x_cen', 'y_cen', 'srs', 'ldt',
                        'cp', 'cm', 'cmc', 'np', 'nm', 'cv', 'tv', 'nv', 'pnp', 'plp',
                        'td', 'es', 'pt', 'pu', 'dp', 'dm']
        df_final = df_final[column_order]
        df_output = pd.concat([df_output, df_final])

    return df_output


if __name__ == '__main__':
    start_time = datetime.datetime.fromtimestamp(time.time())

    df_referencias_input = pd.read_excel(os.path.join(INPUT_PATH, "input.xlsx"))

    # Miramos si el dataframe tiene registros y, si los tiene,
    # cargamos la lista de referencias de la columna "ReferenciaCatastral"
    if len(df_referencias_input) > 0:
        list_referencias_input = df_referencias_input["ReferenciaCatastral"].tolist()
        df_output = api_catastro_referencias_catastrales(list_referencias_input)

        date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        df_output.to_excel(os.path.join(OUTPUT_PATH, f'{date}_outputCatastro.xlsx'), index=False)
    else:
        print("No tenemos referencias en el excel. "
              "Asegurate de que la columna ReferenciaCatastral existe y tiene al menos una referencia. \n")

    # Acabamos y calculamos el tiempo de ejecución:
    print(f"Terminado en {datetime.datetime.now() - start_time}.")
