import neurokit2 as nk


# Heart class to represent the heart model, generates ecg given heart rate (by default 80)
class Heart:
    def __init__(self, heart_rate=80):
        self.heart_rate = heart_rate
        # duration: length of ecg in seconds
        # sampling_rate: number of samples per sec
        self.ecg_signal = nk.ecg_simulate(duration=10, noise=0.05, heart_rate=self.heart_rate, method='ecgsyn',
                                          sampling_rate=3000)

    def getDiagnostics(self):
        return self.ecg_signal, self.heart_rate

    def getECG(self):
        return self.ecg_signal
