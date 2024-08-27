import pandas as pd
import sys

def generar_tablas_latex(file_path):
    # Lee el archivo CSV en un DataFrame de pandas
    df = pd.read_csv(file_path)
    
    # Obtiene las combinaciones únicas de la columna 'Combinación'
    combinaciones = df['Combinación'].unique()
    
    # Inicializa el código LaTeX
    latex_code = r"\documentclass{article}" + "\n" + r"\usepackage{float}" + "\n" + r"\usepackage{caption}" + "\n" + r"\begin{document}" + "\n\n"
    
    for comb in combinaciones:
        # Filtra el DataFrame por la combinación actual y obtiene las primeras 10 filas
        comb_df = df[df['Combinación'] == comb].head(10)
        
        # Añade el encabezado de la tabla LaTeX
        latex_code += r"\begin{table}[H]" + "\n" + r"\centering" + "\n"
        latex_code += f"\\caption{{Resultados para la Combinación {comb}}}" + "\n"
        latex_code += r"\begin{tabular}{|c|c|c|}" + "\n" + r"\hline" + "\n"
        latex_code += r"\textbf{Ejecución} & \textbf{Combinación} & \textbf{Resultado} \\" + r"\hline" + "\n"
        
        # Añade las filas de datos a la tabla LaTeX
        for index, row in comb_df.iterrows():
            latex_code += f"{row['Ejecución']} & {row['Combinación']} & {row['Resultado']} \\\\" + "\n" + r"\hline" + "\n"
        
        # Cierra la tabla LaTeX
        latex_code += r"\end{tabular}" + "\n" + r"\end{table}" + "\n\n"
        
        # Inserta un salto de página cada 4 tablas
        if (combinaciones.tolist().index(comb) + 1) % 4 == 0:
            latex_code += r"\newpage" + "\n\n"
    
    # Cierra el documento LaTeX
    latex_code += r"\end{document}"





    with open('output.tex', 'w') as f:
        f.write(latex_code)
    print("Archivo LaTeX generado: output.tex")

# Funcion para leer desde el bash    
if __name__ == "__main__":
    # Verifica que se haya proporcionado un argumento
    if len(sys.argv) != 2:
        print("Uso: python3 generar_tablas.py <ruta_al_archivo_csv>")
    else:
        # Obtiene la ruta del archivo CSV desde los argumentos
        file_path = sys.argv[1]
        # Genera las tablas LaTeX
        generar_tablas_latex(file_path)
