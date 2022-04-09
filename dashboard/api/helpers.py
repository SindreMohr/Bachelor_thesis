# importing sys so we can find ML_classes
import sys
  
# adding ML_classes to the system path
sys.path.insert(0, '../../')

from ML_classes.DTModel import DTModel
from ML_classes.LSTMModel import LSTMModel
from ML_classes.MLPModel import MLPModel

from keras.models import load_model


def retrieve_DT():
    pass

def retrieve_MLP(mid,lag,batches,epochs,train_test_split):
    deep_learner = MLPModel(
    data = hh,
    Y_var = 'energy',
    lag = lag,
    layer_layer_depths = [30],
    layer_count= 1,
    epochs = epochs,
    batch_size = batches,
    train_test_split = train_test_split
    )
    f = load_model("./saved_models/mlp_model")

def retrieve_LSTM():
    pass

def run_DT(data,lag,train_test,epoch):

    DT = DTModel(
    data = data,
    Y_var = 'energy',
    lag = lag,
    epochs = epoch,
    batch_size = 256,
    train_test_split = train_test
    )
    #training
    DT.DTModel()
    print("done training")
    model_result_dict = {}
    model_result_dict["predictions"] = DT.predict()
    model_result_dict["mse"] = DT.eval.MSE()
    model_result_dict["rmse"] = DT.eval.RMSE()
    model_result_dict["mae"] = DT.eval.MAE()
    model_result_dict["mape"] = DT.eval.MAPE()

    peaks, peak_dates, peak_indexes, res = DT.eval.peak_daily_consumption()
    model_result_dict["daily_peaks"] = peaks
    model_result_dict["daily_peak_dates"] = peak_dates
    model_result_dict["daily_peaks_indexes"] = peak_indexes
    model_result_dict["daily_peaks_res"] = res

    return model_result_dict

def run_LSTM(data,lag,train_test,epoch):

    LSTM = LSTMModel(
        data = data,
        Y_var = 'energy',
        lag = lag,
        LSTM_layer_depths = [50],
        epochs =epoch,
        batch_size = 256,
        train_test_split = train_test
    )
    #training
    LSTM.LSTModel()

    print("done training")
    model_result_dict = {}
    model_result_dict["predictions"] = LSTM.predict()
    model_result_dict["predictions"] =   [ float(x) for x in  model_result_dict["predictions"] ]

    model_result_dict["mse"] = LSTM.eval.MSE()
    model_result_dict["rmse"] = LSTM.eval.RMSE()
    model_result_dict["mae"] = LSTM.eval.MAE()
    model_result_dict["mape"] = LSTM.eval.MAPE()

    peaks, peak_dates, peak_indexes, res = LSTM.eval.peak_daily_consumption()
    model_result_dict["daily_peaks"] = peaks
    model_result_dict["daily_peak_dates"] = peak_dates
    model_result_dict["daily_peaks_indexes"] = peak_indexes
    model_result_dict["daily_peaks_res"] = res


    return model_result_dict

def run_MLP(data,lag,train_test,epoch):

    MLP = MLPModel(
        data = data,
        Y_var = 'energy',
        lag = lag,
        layer_depths = [30],
        layer_count= 1,
        epochs =epoch,
        batch_size = 256,
        train_test_split = train_test
    )
    #training
    MLP.MLPModel()

    print("done training")
    model_result_dict = {}
    model_result_dict["predictions"] = MLP.predict()
    model_result_dict["predictions"] =   [ float(x) for x in  model_result_dict["predictions"] ]


    model_result_dict["mse"] = MLP.eval.MSE()
    model_result_dict["rmse"] = MLP.eval.RMSE()
    model_result_dict["mae"] = MLP.eval.MAE()
    model_result_dict["mape"] = MLP.eval.MAPE()

    peaks, peak_dates, peak_indexes, res = MLP.eval.peak_daily_consumption()
    model_result_dict["daily_peaks"] = peaks
    model_result_dict["daily_peak_dates"] = peak_dates
    model_result_dict["daily_peaks_indexes"] = peak_indexes
    model_result_dict["daily_peaks_res"] = res

    #print(type(model_result_dict["mse"]))
    #print(type(model_result_dict["predictions"][0]))
    #print(type(model_result_dict["daily_peaks"][0]))
    #print(type(model_result_dict["daily_peak_dates"][0]))
    return model_result_dict