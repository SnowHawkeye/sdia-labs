from pylab import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sklearn as skl

class BinaryPointsClassificationPresenter():
    """Utility class to help with displaying prediction results and error rates.
    """

    def __init__(self, test_data, test_target, f_predict):
    
        self.test_data = test_data
        self.test_target = test_target
        self.f_predict = f_predict
        
        self.prediction = self.f_predict(test_data)
        self.errors, self.error_rate = self.__errors()
        
        self.confusion_matrix = skl.metrics.confusion_matrix(self.test_target, self.prediction)
        
        
    def __errors(self):
        """Returns the points that were classified wrongly and the error rate.
        """
        
        is_wrong_prediction = np.logical_or(np.logical_and(self.prediction[:] == 1, self.test_target[:] == 0), np.logical_and(self.prediction[:] == 0, self.test_target[:] == 1))
        errors = self.test_data[is_wrong_prediction, :][:,1:]
        error_rate = len(errors) / len(self.test_data)
        
        return errors, error_rate

    def predicted_points_figure(self, title=""):
        """Given a set of points and binary predictions (0-1), returns a graph showing the classification, crossing out the mistakes.
        """
        
        x_predicted_0 = self.test_data[self.prediction[:] == 0, :][:,1:]
        x_predicted_1 = self.test_data[self.prediction[:] == 1, :][:,1:]

        plt.scatter(x_predicted_0[:,0], x_predicted_0[:,1], c='r')
        plt.scatter(x_predicted_1[:,0], x_predicted_1[:,1], c='g')
        plt.scatter(self.errors[:,0], self.errors[:,1], c='b', marker = 'x')
        plt.title(title + "\n(mistakes are crossed out in blue)")
        
        
    def decision_regions_figure(self, x1_bounds, x2_bounds, resolution=1000):
        """Displays the decision regions for a given resolution (number of points along each axis).
        """

        x1 = np.linspace(x1_bounds[0], x1_bounds[1], resolution) 
        x2 = np.linspace(x2_bounds[0], x2_bounds[1], resolution) 
        X1, X2 = meshgrid(x1,x2)
        
        X = np.stack((np.ones(resolution**2), np.ravel(X1), np.ravel(X2))).T
        Z = self.f_predict(X).reshape(X1.shape)

        plt.contourf(X1, X2, Z, colors=['r', 'g', 'b', "y", 'purple'], alpha = 0.3) # extra colors are necessary otherwise everything is green and the boundary is red         
        
        
    def confusion_matrix_heatmap(self):
        """Displays the heatmap corresponding to the confusion matrix."""
        sns.heatmap(self.confusion_matrix, annot=True, fmt='d', cmap=plt.cm.Purples, xticklabels=['red', 'green'], yticklabels=['red', 'green'])      
         
        
    def display_prediction(self, x1_bounds, x2_bounds, resolution = 1000, figsize=(20,5) , title = "Classification"):
        """Convenient all-in-one display function. Displays the decision regions, the classified points (with mistakes) and the confusion matrix heatmap.
        """
        
        plt.figure(figsize=figsize)

        plt.subplot(121)
        self.predicted_points_figure(title)
        self.decision_regions_figure(x1_bounds, x2_bounds, resolution)

        plt.subplot(122)
        plt.title("Confusion matrix\nThe X axis corresponds to predicted labels")
        self.confusion_matrix_heatmap()