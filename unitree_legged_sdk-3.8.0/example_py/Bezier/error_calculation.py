    
def error (oscillator_data,freq_command):
#computing MAE and MSE

    n= len(oscillator_data)
    assert (len(oscillator_data) == len(freq_command))
    sum_absolute_error = 0
    squarred_error = 0
    maximum_error = -1
    for i in range(n): 
        absolute_error = abs(oscillator_data[i] - freq_command[i] )
        sum_absolute_error += absolute_error
        if absolute_error> maximum_error : 
            maximum_error = absolute_error
        
        squarred_error+= (oscillator_data[i] - freq_command[i]) * (oscillator_data[i] - freq_command[i])
        
    amplitude = max(freq_command) - min(freq_command)
    result_MAE = sum_absolute_error / n
    result_MSE = squarred_error / n
    relative_MAE = result_MAE / amplitude

    return maximum_error, result_MAE, result_MSE, relative_MAE