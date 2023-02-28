from sklearn import metrics as met
import pandas as pd
from mlxtend.evaluate import lift_score
import scikitplot as skplt
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer
import seaborn as sns
import scipy.stats as ss
import statsmodels.stats.proportion as sp

##### EXPLORATORY DATA ANALYSIS #####


def frequency_table(df, feature):

    """ This function receives a dataframe and a categorical variable and returns a frequency table."""

    table = {}
    percentage = round(df[feature].value_counts(normalize=True)*100, 2)
    freq = df[feature].value_counts()
    for i in range(len(percentage.index)):
        table[percentage.index[i]] = [freq[i], percentage[i]]


    freq_table = pd.DataFrame(table).T.rename(columns={0: 'freq', 1: '%'})
    freq_table['%acum'] = freq_table['%'].cumsum()

    return freq_table


def cohort_plot(df, num_var, response):

    """
    This function receives a data frame, a numeric variable, and the target variable. It then plots a cohort plot with the percentage of positive labels in each cohort of the numeric variable.
    """

    # Defines 10 quantiles of the numeric variable (10 cohorts).
    groups = pd.qcut(df[num_var], q=10, duplicates='drop')

    # Percentage of interested customer in each cohort
    df_plot = df.groupby(groups).mean(numeric_only=True)[[num_var, response]].rename(columns={response: 'interested %'})
    df_plot['interested %'] = df_plot['interested %']*100

    sns.lineplot(x=num_var, y='interested %', data=df_plot)
    plt.title(f'{num_var.capitalize()} x Interested %')



def categorical_cohort_summary(df, cat_col, target, transform=True):
    """
    This function receives a data frame, the column name of a categorical variable, and the column name of the target variable. It then computes the proportion and the confidence interval of positive labels (target) for each class of the categorical variable.

    Args:
        df (DataFrame): data frame
        cat_col (string): name of the column of the categorical variable
        target (string): name of the column of the target variable
        transform (bool, optional): Whether to transform the categorical column into Yes and No classes. Defaults to True.

    Returns:
        DataFrame: A data frame with the proportion of positive labels and the lower and higher limits of the confidence interval for each class of the categorical variable.  
    """
    df = df.copy()
    if df[cat_col].dtype == 'int64' and transform:
        df[cat_col] = df[cat_col].apply(lambda x: 'Yes' if x == 1 else 'No')

    summary = df.groupby(cat_col).agg({cat_col:'count', target: ['sum', 'mean']})
    intervals = sp.proportion_confint(summary[(target, 'sum')],
                                      summary[(cat_col, 'count')],
                                      method='wilson')
    summary[cat_col + '_percent'] = (1.0/df.shape[0]*summary[(cat_col, 'count')])

    summary['lo_conf'] = intervals[0]
    summary['hi_conf'] = intervals[1]

    summary['lo_int'] = summary[(target, 'mean')] - summary['lo_conf']
    summary['hi_int'] = summary['hi_conf'] - summary[(target, 'mean')]

    return summary


def cohort_plot_cat(df, cat_col, target, transform=True):
        
    """
    This function plots the cohort plot of a categorical variable with the values obtained with the `categorical_cohort_summary` function.
    """

    summary = categorical_cohort_summary(df, cat_col, target, transform)
    n_category = summary.shape[0]
    plt.bar(x=summary.index, label=cat_col, color=['blue', 'orange'],height=summary[(target, 'mean')], yerr=summary[['lo_int', 'hi_int']].T.values, capsize=80/n_category)
    plt.title(f'Interest by {cat_col}', fontsize=20)
    plt.xlabel(cat_col)
    plt.ylabel('Category Interest Rate')
    plt.grid()

def cohort_2v_cat_plot(df, cat_col_1, cat_col_2):

    """
     This function computes the proportion of positive labels (target) and the confidence interval for each combination of classes of the two categorical variables. It then plots the cohort plot of the two categorical variables combined.
    """
    summary = df.groupby([cat_col_1, cat_col_2]).agg({'id':'count', 'response': ['sum', 'mean']})
    intervals = sp.proportion_confint(summary[('response', 'sum')], summary[('id', 'count')], method='wilson')

    summary['lo_conf'] = intervals[0]
    summary['hi_conf'] = intervals[1]

    summary['lo_int'] = summary[('response', 'mean')] - summary['lo_conf']
    summary['hi_int'] = summary['hi_conf'] - summary[('response', 'mean')]

    summary = summary.reset_index()

    n_category = summary.shape[0]

    sns.barplot(data=summary, x=cat_col_1, hue=cat_col_2, y=summary[('response', 'mean')], ci=95, capsize=80/n_category,)
    plt.ylabel('Interest %')

def cramer_v(x, y):

    """
    This function receives two categorical variables (arrays). It then computes the association between them using the Cramer V method.
    """
    cm = pd.crosstab(x, y)
    return ss.contingency.association(cm, method='cramer', correction=True)


def object_trans(df):

    return df.astype('object')


##### MACHINE LEARNING MODELLING ########
def prc_auc(y_val, y_prob):

    """
    This function calculates the area under the curve of the precision-recall curve (PRC_AUC)
    
    Arguments:

    y_val (array): an array or a list of actual target values.
    y_prob (array): an array or a list of class probabilities.
 

    Returns:
        Float: Return the value of th metric PRC_AUC.
    """
    lr_precision, lr_recall, _ = met.precision_recall_curve(y_val, y_prob)
    prc_auc = met.auc(lr_recall, lr_precision)

    return prc_auc

def precision_at_k(y_true, y_score, k=20000):

    """
    This function calculates the precision at k, which is the ratio of true positive predictions to the total number of positive predictions made.

    Arguments:

    y_true (array): an array or a list of actual target values
    y_score (array): an array or a list of class probabilities
    k (int): the number of top predictions to consider

    Returns:
        float: Return the precision at k.
    """
    if type(y_true) != np.ndarray:

        try:
            y_true = np.array(y_true.copy())

        except:
            print('y_true needs to be an array, list or Series')
    else:
        pass

    sorted_index = np.argsort(y_score)[::-1]
    
    precision_at_k = np.cumsum(y_true[sorted_index])/np.arange(1, len(y_score)+1)

    return precision_at_k[k]


def recall_at_k(y_true, y_score, k=20000):

    """
    This function calculates the recall at k, which is the ratio of true positive predictions to the total number of actual positive examples.

    Arguments:

    y_true (array): an array or a list of actual target values
    y_score (array): an array or a list of class probabilities
    k (int): the number of top predictions to consider

    Returns:
        float: Return the precision at k.
    """
    if type(y_true) != np.ndarray:

        try:
            y_true = np.array(y_true.copy())

        except:
            print('y_true needs to be an array, list or Series')
    else:
        pass
    
    sorted_index = np.argsort(y_score)[::-1]
    
    recall_at_k = np.cumsum(y_true[sorted_index])/np.sum(y_true[sorted_index])

    return recall_at_k[k]

def scores_summary(scores_dict, classifier_name):

    """
    This function receives the name of a classifier, and a dictionary of evaluation metric scores computed using cross-validation.
    It then calculates the average and the 95% confidence interval (ci) for each metric, and stores the values in a dictionary. 

    Args:
        scores_dict (dict): Dictionary with .
        classifier_name (string): Name of the classifier

    Returns:
        Dataframe: Summary dataframe with the name of the classifier and the mean and ci of each score in the dictionary.
    """
    dic = {}

    for metric, scores in scores_dict.items():
        mean = scores.mean()
        std = scores.std()
        ci = 1.96*std
        dic[metric] = f'{round(mean, 4)} +/- {round(ci, 4)}'
    
    return pd.DataFrame(dic, index=[classifier_name])


def classifier_metrics_test(clf_name, y_val, yhat_, y_prob, k):  

    """
    This function receives the classifier name, the true label y_val, the label predicted by the model (y_hat_), the score given by the the value of k to calculate precision/recall at k.

        Then it computes several evaluation metrics.

    Arguments:
        clf_name (string): Classifier's name.
        y_val (array): an array or a list of actual target values.
        y_hat_ (array): an array or a list of predict class values.
        y_prob (array): an array or a list of class probabilities.
        k (int): the number of top predictions to consider.
    Returns:

        DataFrame: A dataframe with the computed scores — balanced_accuracy, f1_score, lift_score, prc_auc, recall, precision, precision_at_k, recall_at_k, and roc_auc.
    """
    precision_k = precision_at_k(y_val, y_prob[:, 1], k)
    recall_k = recall_at_k(y_val, y_prob[:, 1], k)
    precision = met.precision_score(y_val, yhat_)
    accuracy = met.balanced_accuracy_score(y_val, yhat_)
    recall = met.recall_score(y_val, yhat_)
    f1_score_ = met.f1_score(y_val, yhat_)
    rocauc = met.roc_auc_score(y_val, y_prob[:, 1])
    lift_score_ = lift_score(y_val, yhat_)
    lr_precision, lr_recall, _ = met.precision_recall_curve(y_val, y_prob[:, 1])
    prc_auc = met.auc(lr_recall, lr_precision)

    return pd.DataFrame({clf_name: {'lift_score': lift_score_, 'precision': precision, 'balanced_accuracy': accuracy, 'recall': recall, 'f1_score': f1_score_, 'roc_auc': rocauc, 'prc_auc': prc_auc, f'precision_at_{k}': precision_k, f'recall_at_{k}': recall_k}}).T



def cross_val_metrics(name, pipeln, X, y,  cv, k):

    """This function receives a classiifer's name, a pipeline object, features X, label y, the number of folds
        for cross-validation (cv), and the value of k to calculate precision/recall at k.

        Then it computes several evaluation metrics using the cross_validate function from scikit-learn.

     Args:

        name (string): Classifier's name.
        pipeline (pipeline object): Pipeline used for the model evaluation.
        X (dataframe): DataFrame with the features used in the model.
        y (array): Labels.
        cv (int): Number of folds for the cross_validate function.
        k (int): Position for precision/recall at k.
        

    Returns:
        DataFrame: A dataframe with the computed scores — balanced_accuracy, f1_score, lift_score, prc_auc, recall, precision, precision_at_k, recall_at_k, and roc_auc.
    """
    scores = cross_validate(pipeln, X, y, cv=cv, scoring={
                                                'balanced_accuracy': make_scorer(met.balanced_accuracy_score),
                                                'f1_score': make_scorer(met.f1_score),
                                                'lift_score': make_scorer(lift_score),
                                                'prc_auc': make_scorer(prc_auc, needs_proba=True),
                                                'recall': make_scorer(met.recall_score, zero_division=True),
                                                'precision': make_scorer(met.precision_score, zero_division=True),
                                                'precision_at_k': make_scorer(precision_at_k, needs_proba=True, k=k),
                                                'recall_at_k': make_scorer(recall_at_k, needs_proba=True, k=k),
                                                'roc_auc': make_scorer(met.roc_auc_score)

                                                })

    scores_sum = scores_summary(scores, name) 
    return scores_sum


def classifier_metrics_plot(y_prob, y_true):

    """
    This function plots 4 graphics — cumulative gain, lift curve, roc curve and precision recall curve — to evaluate the performance of a classifier.
    """

    fig, axis = plt.subplots(2, 2, figsize=(20, 12))
    
    skplt.metrics.plot_cumulative_gain(y_true, y_prob, ax=axis[0, 1])
    skplt.metrics.plot_lift_curve(y_true, y_prob, ax=axis[0, 0])
    skplt.metrics.plot_roc(y_true, y_prob, ax=axis[1, 0])
    skplt.metrics.plot_precision_recall_curve(y_true, y_prob, ax=axis[1, 1])

    plt.tight_layout()


#### BUSINESS PERFORMANCE #####
def business_eval(scenario, n_customers, perc_of_interested_customers, target_percentage, n_calls, revenue_per_customer):

    """
    This function calculates the business performance 
    """

    reached_targets = int(n_customers*perc_of_interested_customers*target_percentage)

    total_revenue = reached_targets*revenue_per_customer


    return pd.DataFrame({'Scenario': scenario,'Number Calls': f'{n_calls:,}', 'Targets Reached': f'{reached_targets:,}', 'Revenue per Customer': f'{revenue_per_customer:,.2f}', 'Total Revenue': f'$ {total_revenue:,.2f}'}, index=[0])


def percentage_of_interested_customers(test_elements, n_calls, n_customers, y_true, y_prob):

    """
    This function calculates the percentage of interested customers that will be reached for a given number of calls.
    """
    base = skplt.metrics.cumulative_gain_curve(y_true, y_prob[:, 1])[0]
    gain = skplt.metrics.cumulative_gain_curve(y_true, y_prob[:, 1])[1]
    
    index = int(test_elements*n_calls/n_customers)

    base_percent, percentage_target_reached = base[index], gain[index]

    return base_percent, percentage_target_reached