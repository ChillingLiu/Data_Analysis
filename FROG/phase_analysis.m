fileNameT = 'retrieved_t';
fileNameET = 'retrieved_Et';
t = dlmread([fileNameT '.txt']);
Et = dlmread([fileNameET '.txt']);
Et = Et/max(abs(Et));

phi = -unwrap(angle(Et));

p = polyfit(t, phi, 2);
x = linspace(min(t), max(t), length(t));
y = polyval(p, x);
p_str = sprintf('%f * x^2 + %f * x + %f', p);

figure(1);
yyaxis left
plot(t, abs(Et), 'black');
yyaxis right
plot(t, phi, 'r');
hold on
plot(x, y, 'r--');
hold off
subtitle(p_str);
legend('Et', 'phi', 'fitted phi');

%figure(2);
%plotcmplx(t,Et);
