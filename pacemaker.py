import random
import neurokit2 as nk


class Pacemaker:

    # Creates pacemaker for a patient given his heart model and desired pacing mode (by default AAI)
    def __init__(self, heartModel, pacing_mode):
        self.heartModel = heartModel
        # functions to extract necessary information from the ecg
        self._, self.rpeaks = nk.ecg_peaks(heartModel.getECG(), sampling_rate=3000)
        self.waves_dict, self.waves_peak = nk.ecg_delineate(heartModel.getECG(), self.rpeaks, sampling_rate=3000,
                                                            method='dwt', show_type="peak")
        if pacing_mode.upper() in ['AAI', 'VVI', 'DDD']:
            self.pacing_mode = pacing_mode
        else:
            print('***** Wrong pacing mode selected, switching to AAI ******')
            self.pacing_mode = 'AAI'

    # paces the heart according to the desired pacing mode
    # returns: paced ecg signal (as an array of voltages)
    def pace(self):
        if self.pacing_mode.upper() == 'AAI':
            return self.__paceUsingAAI()
        elif self.pacing_mode.upper() == 'VVI':
            return self.__paceUsingVVI()
        elif self.pacing_mode.upper() == 'DDD':
            return self.__paceUsingDDD()

    # paces the heart using AAI pacing mode
    # returns: paced ecg signal (as an array of voltages)
    def __paceUsingAAI(self):
        ecg_signal_paced = self.heartModel.getECG().copy()
        i = 0
        # triggers if p-wave peak is less than 0.25mV, else inhibits
        for index in self.waves_peak['ECG_P_Peaks']:
            if ecg_signal_paced[index] < 0.25:
                ecg_signal_paced[self.waves_peak['ECG_P_Onsets'][i]] = 0.7
            i = i + 1
        return ecg_signal_paced

    # paces the heart using VVI pacing mode
    # returns: paced ecg signal (as an array of voltages)
    def __paceUsingVVI(self):
        # generate the abnormal heart beats (without qrs complex)
        ecg_signal_paced = self.__generateAbnormality()
        # triggers if qrs-wave peak is less than 1mV, else inhibits
        for i in self.rpeaks['ECG_R_Peaks']:
            if ecg_signal_paced[i] < 1:
                ecg_signal_paced[i] = 1.5
        return ecg_signal_paced

    # paces the heart using VVI pacing mode
    # returns: paced ecg signal (as an array of voltages)
    def __paceUsingDDD(self):
        # generate the abnormal heart beats (without qrs complex)
        ecg_signal_paced = self.__generateAbnormality()
        # triggers if qrs-wave peak is less than 1mV, else inhibits
        for i in self.rpeaks['ECG_R_Peaks']:
            if ecg_signal_paced[i] < 1:
                ecg_signal_paced[i] = 1.5
        i = 0
        # triggers if p-wave peak is less than 0.25mV, else inhibits
        for index in self.waves_peak['ECG_P_Peaks']:
            if ecg_signal_paced[index] < 0.25:
                ecg_signal_paced[self.waves_peak['ECG_P_Onsets'][i]] = 0.7
            i = i + 1
        return ecg_signal_paced

    # Generates the abnormal heart beats (randomly deletes at least 3 qrs complexes)
    def __generateAbnormality(self):
        ecg_signal = self.heartModel.getECG()
        n = random.randrange(3, len(self.waves_peak['ECG_Q_Peaks']) - 2)
        rand_indices_list = random.choices(range(0, len(self.waves_peak['ECG_Q_Peaks'])), k=n)
        rand_indices = set(rand_indices_list)
        for i in rand_indices:
            s_index = self.waves_peak['ECG_S_Peaks'][i]
            while ecg_signal[s_index] <= ecg_signal[self.waves_peak['ECG_R_Onsets'][i]]:
                s_index = s_index - 1
            for x in range(self.waves_peak['ECG_R_Onsets'][i], s_index):
                ecg_signal[x] = ecg_signal[self.waves_peak['ECG_R_Onsets'][i]]
        return ecg_signal.copy()
