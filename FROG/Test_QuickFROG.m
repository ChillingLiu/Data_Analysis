function Test_QuickFROG3(varargin)
clear;
close all

fileName = 'chosen_0';
Data = dlmread([fileName '.txt']);
Asig = abs(Data);
%Asig = quickscale(Asig);
N = length(Data);

fileName = 'time_delay_chosen_0';
t = dlmread([fileName '.txt']);
lent = max(t) - min(t);
t = (-lent/2: lent/(N-1): lent/2);
fileName = 'wavelength_chosen_0';
w = dlmread([fileName '.txt']);
%w = 300./w;


% ------------- our data + jocobian transformation -------------
data = importdata("FlashWave.txt");
lambda_ = data(:,1); % wavelength
I_lambda_ = data(:,2);

frequency = 300./lambda_;
I_freq = I_lambda_ .* 300 ./ (frequency.^2);

Et = ifftshift( ifft( ifftshift(I_freq) ) );
%Et = fftshift( fft( ifftshift(I_freq) ) );
Et = Et./max(Et);
Center = round(length(Et)./2);
n2 = round(N/2);
Et = Et(Center - n2 + 1: Center + n2);

%Et = pulsegenerator(N); Et = complex(abs(Et));
Et = QuickFROG_tT(Asig, Et, t, w);
