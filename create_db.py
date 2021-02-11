import pandas as pd
from sqlalchemy import create_engine


def import_list(force=''):
    engine = create_engine('sqlite:///app.db', echo=False)

    url = 'http://www.ik2ane.it/pontixls.xls'
    df = pd.read_excel(url)
    # %%
    df = df.dropna(subset=['(F)req'])
    # %%
    df = df.drop(['Agg.', '(K)m', 'Gradi', '(O)rdkey', 'JN45OL'], axis=1)
    # %%
    df.dropna(subset=['(N)ome'], inplace=True)

    # Write to SQL
    df.to_sql('ponti', con=engine, if_exists='replace')


    return True

if __name__ == "__main__":
    import_list()
