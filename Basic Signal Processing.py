import math

class midexam:
     
    def __init__(self,name): # file name  
        self.name=name
    
    def load_data(self): # load data
        file=open(self.name,'r')
        lines=file.readlines()
        time,emg=[],[]
        for i in lines:
            time.append(float(i.split(" ")[3]))
            emg.append(float(i.split(" ")[-1]))
        import matplotlib.pyplot as plt
        plt.plot(time,emg)
        plt.show()
        return time, emg
        
    def FFT(self, data, fs): # FFT function
        import numpy as np
        length=len(data)
        k=np.arange(length)
        T=length/fs
        freq=k/T
        freq=freq[range(int(length/2))]
        data_fft=np.fft.fft(data)
        data_fft=abs(data_fft[range(int(length/2))])
        for i in range (len(data_fft)):
            if data_fft[i]>data_fft[i-1] and data_fft[i]>data_fft[i+1] and data_fft[i]>200:
                print(freq[i])
        return freq,data_fft
    
    def high_Freq_response(self,data,fs): # Highpass_filter + freq_response
        import scipy.signal as ssig
        b,a= ssig.butter(6,200,btype='high',fs=fs)
        w,h=ssig.freqz(b,a,fs)
        w_hz=w*fs/(2*math.pi)
        high_data=ssig.filtfilt(b,a,data)
        return w_hz, abs(h), high_data
    
    def RMS_processing(self,data,fs): # rms processing  for envelope 
        rms_data=[]
        for i in range(0,len(data)):
            slist=[x**2 for x in data[i:i+int(0.01*fs)]]
            s2_list=math.sqrt(sum(slist)/len(slist))
            rms_data.extend([s2_list])
        return rms_data

    def show_result(self): # show result 
        time,data=midexam.load_data(self)
        fs=int(1/(time[1]-time[0]))
        fft_freq,fft_data=midexam.FFT(self,data,fs) # 2.1.(1)
        w_hz, fr_h,high_data=midexam.high_Freq_response(self,data,fs) # 2.3.(1) / 2.3.(2)
        fft_high_freq,fft_high_data=midexam.FFT(self,high_data,fs) # 2.4.(1) 
        rms_data=midexam.RMS_processing(self,high_data,fs) # 2.5
        # Spectrogram 2.1.(2): row-56  2.4.(2): row-60
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10,8))
        plt.subplot(4,2,1);plt.plot(fft_freq,fft_data,'black');plt.title("2.1.(1) Signal using FFT"); plt.xlabel('frequency(hz)');plt.xlim([0,1000])
        plt.subplot(4,2,2);plt.specgram(data,Fs=fs);plt.title("2.1.(2) Signal using spectrogram"); plt.xlabel('time'); plt.ylabel('frequency');
        plt.subplot(4,2,3);plt.plot(w_hz,fr_h,'black');plt.title("2.3.(1) Frequency response"); plt.xlabel('freq'); plt.ylabel('|H(jw)|');plt.xlim([0,1000])
        plt.subplot(4,2,4);plt.plot(time,high_data,'black');plt.title("2.3.(2) Signal after filtering");plt.xlabel('time'); plt.ylabel('Amplitude');
        plt.subplot(4,2,5);plt.plot(fft_high_freq,fft_high_data,'red');plt.title("2.4.(1) Filterd signal using FFT"); plt.xlabel('frequency(hz)');plt.xlim([0,1000])
        plt.subplot(4,2,6);plt.specgram(high_data,Fs=fs);plt.title("2.4.(2) Filterd signal using spectrogram"); plt.xlabel('time'); plt.ylabel('frequency');
        plt.subplot(4,1,4);plt.plot(time,high_data,'black',label="Filterd signal");plt.plot(time,rms_data,'red',label="Envelope");plt.title("2.5 Envelope of Signal"); plt.xlabel('time(s)'); plt.ylabel('amplitude(mV)');
        plt.legend();plt.tight_layout();plt.show()

if __name__=="__main__":
    midexam('data.txt').show_result()