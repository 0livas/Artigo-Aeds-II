import pandas as pd

def tratar_csv_1(input_file, output_file, delimiter=';'):
    df = pd.read_csv(input_file)
    #Shows the first lines just to see how it is going.
    print(df.head())
    df.to_csv(output_file, sep=delimiter, index=False)
    print(f"O arquivo foi salvo como: {output_file}")
    

def tratar_csv_2(input_file, output_file, delimiter = ';'):
    # 1. Carregar o dataset original
    df = pd.read_csv(input_file, sep=delimiter)

    # 2. Remover a coluna 'education'
    df = df.drop(columns=['education'])

    # 3. Filtrar apenas os pacientes com TenYearCHD == 1
    df = df[df['TenYearCHD'] == 1]

    # 4. Salvar o novo dataset sem a coluna 'education' e apenas com pacientes positivos
    df.to_csv(output_file, sep=delimiter, index=False)

    print(f"Novo arquivo salvo: {df.shape[0]} pacientes restantes após o filtro.")