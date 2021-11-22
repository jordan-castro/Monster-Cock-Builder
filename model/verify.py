import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import sys


# The path to the schemas data file
SCHEMAS_PATH = 'data/schemas.txt'
VALID_TYPES = ['Circles', 'Curves', 'Squares', 'Stripes']


def format_skip_values(df):
    """
    Formats the Skip Values of the dataframe.

    # Important:
        - The skip value is taken from the first value of the skip.

    # Arguments
        df: The dataframe to format
    """
    return df["Skip Values"].map(lambda x: int(x.split(",")[0]))


def format_data(df):
    """
    Formats the dataframe data.

    # Arguments
        df: The dataframe to format

    # Returns
        The formatted dataframe
    """
    df = pd.get_dummies(df, columns=["Type"])
    # If result is 0 then it is valid, else 0 (invalid) 
    df.Result = df.Result.map(lambda x: 1 if x == 0 else 0)
    # Currently not using Skip Type
    df = df.drop(columns=['Skip Type'], axis=1)
    df['Skip Values'] = format_skip_values(df)
    return df


class Verifier: # TODO: Clustering with Kmeans
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
        self.knn = KNeighborsClassifier()
        self.data = pd.read_csv(SCHEMAS_PATH, sep=';')

    def scale_data(self, df):
        # Scale the data frame
        features = [["Modulus", "Size", "Skip Values"]]
        for feature in features:
            df[feature] = self.scaler.fit_transform(df[feature])
        return df

    def verify(self, data):
        # Make a prediction and return the result
        prediction = self.knn.predict(self.convert_to_dataframe(data))
        # print(prediction)
        return prediction[0]

    def train_model(self):
        # Format and scale data
        self.data = format_data(self.data)
        self.data = self.scale_data(self.data)
        # Split data into training and testing data
        X = self.data.drop(columns=['Result'], axis=1)
        y = self.data['Result']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)

        # Train the model
        self.knn.fit(X_train, y_train)
        # Predict
        y_pred = self.knn.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))

    def accuracy(self, prediction):
        """
        Get the accuracy of a prediction.

        # Arguments
            prediction: The prediction to check.

        # Returns
            The accuracy of the prediction.
        """
        pass
        # return accuracy_score(self.data['Result'], prediction)

    def convert_to_dataframe(self, data):
        """
        Converts a dictionary to a dataframe.

        # Arguments
            data: The dictionary to convert.
        
        # Returns
            The dataframe.
        """
        data_dict = {
            "Modulus": data['Modulus'],
            "Size": data['Size'],
            "Skip Values": data['Skip Values'],
            "Type_Circles": 1 if data['Type'] == 'Cirles' else 0,
            "Type_Curves": 1 if data['Type'] == 'Curves' else 0,
            "Type_Squares": 1 if data['Type'] == 'Squares' else 0,
            "Type_Stripes": 1 if data['Type'] == 'Stripes' else 0,
        }
        # Convert to dataframe and format data
        df = pd.DataFrame(data_dict, index=[0])
        df['Skip Values'] = format_skip_values(df)
        # df = self.scale_data(df)
        return df


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 5:
        print("Invalid number of arguments")
        exit(1)

    # Grab the data from the args
    schema_type = args[0]
    modulus = int(args[1])
    size = int(args[2])
    skip_values = args[3]
    skip_type = args[4]

    data = {
        "Type": schema_type,
        "Modulus": modulus,
        "Size": size,
        "Skip Values": skip_values,
        "Skip Type": skip_type
    }
    verifier = Verifier()
    verifier.train_model()
    prediction = verifier.verify(data)
    # Return the prediction to the CMD
    print(prediction)
