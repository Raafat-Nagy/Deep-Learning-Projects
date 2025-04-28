import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

class ClassificationMetrics:
    """
    A class for calculating and visualizing classification metrics including confusion matrix and classification report.
    
    Attributes:
    ----------
    true_labels : list
        A list of the true class labels (ground truth).
    pred_labels : list
        A list of the predicted class labels.
    class_names : list, optional
        A list of class names for labeling the confusion matrix and classification report.
    
    Methods:
    -------
    plot_confusion_matrix(figsize=None, cbar=False, x_rotation=0, y_rotation=0):
        Generates and displays a confusion matrix heatmap.
        
    classification_report():
        Returns the classification report (precision, recall, f1-score, etc.) as a string.
        
    display_classification_report():
        Prints the classification report to the console.
    """
    
    def __init__(self, true_labels, pred_labels, class_names=None):
        """
        Initializes the ClassificationMetrics object with true and predicted labels and optional class names.
        
        Parameters:
        -----------
        true_labels : list
            The true labels (ground truth) of the dataset.
        pred_labels : list
            The predicted labels by the model.
        class_names : list, optional
            The class names for labeling (default is None).
        """
        self.true_labels = true_labels
        self.pred_labels = pred_labels
        self.class_names = class_names

    def plot_confusion_matrix(self, figsize=None, cbar=False, x_rotation=0, y_rotation=0):
        """
        Generates a confusion matrix heatmap using the true and predicted labels.
        
        Parameters:
        -----------
        figsize : tuple, optional
            The size of the figure (default is None).
        cbar : bool, optional
            Whether to include a color bar (default is False).
        x_rotation : int, optional
            The rotation angle for the x-axis labels (default is 0).
        y_rotation : int, optional
            The rotation angle for the y-axis labels (default is 0).
        """
        cm = confusion_matrix(self.true_labels, self.pred_labels)

        plt.figure(figsize=figsize)
        class_names = self.class_names or "auto"
        ax = sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            square=True,
            linewidths=0.5,
            xticklabels=class_names,
            yticklabels=class_names,
            cbar=cbar,
        )

        # Adding black border around the entire heatmap
        ax.set_frame_on(True)
        ax.patch.set_edgecolor('black')
        ax.patch.set_linewidth(2)

        plt.title("Confusion Matrix")
        plt.xlabel("Predicted Labels")
        plt.ylabel("Actual Labels")
        plt.xticks(rotation=x_rotation)
        plt.yticks(rotation=y_rotation)
        plt.tight_layout()
        plt.show()

    def classification_report(self):
        """
        Returns the classification report for the given true and predicted labels.
        
        Returns:
        --------
        str
            The classification report (precision, recall, f1-score, etc.).
        """
        report = classification_report(self.true_labels, self.pred_labels, target_names=self.class_names)
        return report

    def display_classification_report(self):
        """
        Prints the classification report to the console.
        """
        print("\t\t\tClassification Report")
        print(self.classification_report())


# Example Usage
if __name__ == "__main__":
    # Sample true and predicted labels
    true_labels = [0, 1, 1, 0, 2, 2, 1, 0, 1, 2]
    pred_labels = [0, 1, 1, 0, 1, 2, 2, 0, 1, 2]

    # Define class names (optional)
    class_names = ["Class 0", "Class 1", "Class 2"]

    # Create an instance of ClassificationMetrics
    metrics = ClassificationMetrics(true_labels, pred_labels, class_names)

    # Plot confusion matrix
    metrics.plot_confusion_matrix(figsize=(8, 6), cbar=True, x_rotation=45, y_rotation=45)
    print()
    # Print classification report
    metrics.display_classification_report()
