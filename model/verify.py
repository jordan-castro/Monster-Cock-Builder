import json
import numpy as np
import pandas as pd
import random

from pandas.core.frame import DataFrame
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
import sys


# The path to the schemas data file
SCHEMAS_PATH = 'data/schemas.txt'
VALID_TYPES = ['Circles', 'Curves', 'Squares',
               'Stripes', 'Crosses', 'Space', 'GSquares']


def random_schema(schema: str):
    """
    Generate a random schema.
    """
    modulus = np.random.randint(2, 30)
    size = np.random.randint(1, 100)

    def get_skip_values():
        # The number of skips
        amount = np.random.randint(1, 10)
        # The possible places
        places = [1, 2, 3, 5, 10]
        # The specific place
        place = random.choice(places)
        values = [i * place for i in range(amount)]

        if len(values) == 0:
            return [2, 3, 4, 5, 6, 7, 8]
        else:
            return values
    skip_values = get_skip_values()
    skip_type = random.choice(["original", "v2"])

    return {
        "Type": schema,
        "Modulus": modulus,
        "Size": size,
        "Skip Values": ','.join(map(str, skip_values)),
        "Skip Type": skip_type
    }


def write_to_schema(schema):
    """
    Write the created schema to a JSON file.
    """
    with open("schema.json", "w") as f:
        json.dump(schema, f)


def format_skip_values(df):
    """
    Formats the Skip Values of the dataframe.

    # Important:
        - The skip value is taken from the first value of the skip.

    # Arguments
        df: The dataframe to format
    """
    def get_mean(data):
        """
        Take a string of numbers seperated by commas.
        Split the string by the commas.
        Find the mean of the numbers.
        """
        numbers = list(map(int, data.split(",")))
        return np.mean(numbers)

    return df["Skip Values"].map(lambda x: get_mean(x))


def format_skip_types(df):
    """
    Formats the skip types of the dataframe.

    # Arguments
        df: The dataframe to format

    # Returns
        The formatted dataframe
    """
    def get_type(data):
        """
        Return the skip type as a number.
        original => 0
        v2 => 1
        """
        # Lower case string
        if data.lower() == "original":
            return 0
        elif data.lower() == "v2":
            return 1

    return df["Skip Type"].map(lambda x: get_type(x))


def format_types(df):
    """
    Formats the dataframe types.

    # Arguments
        df: The dataframe to format

    # Returns
        The formatted dataframe
    """
    def get_type(data):
        """
        Return the Schema type as a number.
        Circles => 0
        Curves => 1
        Squares => 2
        Stripes => 3
        """
        # So that we only have to update the VALID_TYPES list and Wazam!
        for t in VALID_TYPES:
            if data.lower() == t.lower():
                return VALID_TYPES.index(t)

    return df["Type"].map(lambda x: get_type(x))


def format_data(df: DataFrame):
    """
    Formats the dataframe data.

    # Arguments
        df: The dataframe to format

    # Returns
        The formatted dataframe
    """
    df['Skip Values'] = format_skip_values(df)
    df['Type'] = format_types(df)
    df['Skip Type'] = format_skip_types(df)

    return df


class Verifier:  # TODO: Clustering with Kmeans
    """
    Class to verify a schema on the MonsterCock-Builder.

    Attributes:
        scaler (MinMaxScaler): The scaler used to normalize the data.
        knn (KNeighborsClassifier): The KNN classifier used to verify the schema.

    Methods:
        train_model(self): Train the model.

    """

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.knn = KNeighborsClassifier(n_neighbors=8)
        self.data = pd.read_csv(SCHEMAS_PATH, sep=';')
        # There are two clusters, one for training and one for verifying
        self.train_cluster = KMeans(n_clusters=8)
        self.verify_cluster = KMeans(n_clusters=1)
        self.features = ["Modulus", "Size", "Skip Values", "Type"]

    def scale_data(self, df):
        # Scale the data frame
        for feature in [self.features + ["Cluster"]]:
            df[feature] = self.scaler.fit_transform(df[feature])
        return df

    def cluster_data(self, df, cluster):
        """
        Cluster the data.
        """
        features = self.features + ["Skip Type"]
        # Fit
        cluster.fit(df[features])
        # Cluster the data based on prediction
        df["Cluster"] = cluster.predict(df[features])

        return df

    def verify(self, data):
        # Make a prediction and return the result
        prediction = self.knn.predict(self.convert_to_dataframe(data))
        # print(prediction)
        return prediction[0]

    def train_model(self):
        # Format and scale data
        self.data = format_data(self.data)
        self.data = self.cluster_data(self.data, self.train_cluster)
        self.data = self.scale_data(self.data)
        # Split data into training and testing data
        X = self.data.drop(columns=['Result'], axis=1)
        y = self.data['Result']
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=4)

        # Train the model
        self.knn.fit(X_train, y_train)
        # Predict
        y_pred = self.knn.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))

    def convert_to_dataframe(self, data):
        """
        Converts a dictionary to a dataframe.

        # Arguments
            data: The dictionary to convert.

        # Returns
            The dataframe.
        """
        # Convert to dataframe and format data
        df = pd.DataFrame(data, index=[0])
        df = format_data(df)
        df = self.cluster_data(df, self.verify_cluster)

        # df = self.scale_data(df)
        return df


if __name__ == "__main__":
    args = sys.argv[1:]

    # Grab the data from the args
    schema = args[0]

    verifier = Verifier()
    verifier.train_model()

    while 1:
        data = random_schema(schema)

        prediction = verifier.verify(data)

        # Check prediction
        if prediction == 1:
            # Convert the values to integers
            data["Skip Values"] = [int(value) for value in data["Skip Values"].split(",")]
            write_to_schema(data)
            break