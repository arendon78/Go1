def error(oscillator_data, freq_command):
    """
    Computes various error metrics between the oscillator data and the frequency command.

    This function calculates the Maximum Absolute Error (Max AE), Mean Absolute Error (MAE),
    Mean Squared Error (MSE), and Relative Mean Absolute Error (Relative MAE) between the
    observed oscillator data and the expected frequency command.

    Parameters
    ----------
    oscillator_data : list of float
        A list containing the observed oscillator frequencies.
    
    freq_command : list of float
        A list containing the commanded (expected) frequencies.

    Returns
    -------
    maximum_error : float
        The maximum absolute error between the oscillator data and the frequency command.
    
    result_MAE : float
        The mean absolute error (MAE) between the oscillator data and the frequency command.
    
    result_MSE : float
        The mean squared error (MSE) between the oscillator data and the frequency command.
    
    relative_MAE : float
        The relative mean absolute error (Relative MAE), which is the MAE normalized by the amplitude
        of the frequency command.

    Raises
    ------
    AssertionError
        If the length of `oscillator_data` and `freq_command` are not equal.
    """

    n = len(oscillator_data)
    assert (len(oscillator_data) == len(freq_command)), "oscillator_data and freq_command must have the same length"
    
    sum_absolute_error = 0
    squared_error = 0
    maximum_error = -1
    
    for i in range(n):
        absolute_error = abs(oscillator_data[i] - freq_command[i])
        sum_absolute_error += absolute_error
        if absolute_error > maximum_error:
            maximum_error = absolute_error
        
        squared_error += (oscillator_data[i] - freq_command[i]) ** 2
        
    amplitude = max(freq_command) - min(freq_command)
    result_MAE = sum_absolute_error / n
    result_MSE = squared_error / n
    relative_MAE = result_MAE / amplitude

    return maximum_error, result_MAE, result_MSE, relative_MAE
