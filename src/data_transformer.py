import pandas as pd


def update_datatypes(data):
    df = pd.DataFrame(data)
    df['published_at'] = pd.to_datetime(df['published_at'])
    df['view_count'] = pd.to_numeric(df['view_count'])
    df['subscriber_count'] = pd.to_numeric(df['subscriber_count'])
    df['video_count'] = pd.to_numeric(df['video_count'])
    return df


def save_to_csv(df, filename):
    df.to_csv(filename, index=False)
