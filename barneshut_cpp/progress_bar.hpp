#include <iostream>
#include <ctime>
class ProgressBar {
public:
    int total;
    int step {0};
    time_t start_time;
    int length;
    ProgressBar(int n, int l){
        total = n;
        length = l;
        start_time = time(0);
    }

    void show_bar(double time_remaining){
        std::cout << '\r';
        std::cout << '[';
        double stepsize = ((double) total)/((double) length);
        for (int i = 0; i < length; i++) {
            if (i * stepsize < step-1 && ((i+1) * stepsize < step-1 || (i+1) * stepsize >= total)) {
                std::cout << "=";
            }
            else if (i * stepsize < step-1){
                std::cout << ">";
            }
            else {
                std::cout << "-";
            }
        }
        char time[20];
        sprintf(time, "%.1f", time_remaining);
        std::cout << "] " << step << '/' << total <<  " (" << time << " s left)";
        if (step == total) std::cout << '\n';
    }

    void show_bar_fancy(double time_remaining){
            std::cout << "\033[32m" << '\r';
        std::cout << '[';
        double stepsize = ((double) total)/100.0;
        for (int i = 0; i < 100; i++) {
            if (i * stepsize < step-1 && ((i+1) * stepsize < step-1 || (i+1) * stepsize >= total)) {
                std::cout << "=";
            }
            else if (i * stepsize < step-1){
                std::cout << "\033[1m\033[34m>\033[0m\033[31m";
            }
            else {
                std::cout << "-";
            }
        }

        if (step == total){
            std::cout << "] " << "\033[1m\033[32m" << step << "/" << total << "\033[0m" <<  " done!"<< std::endl;
        } else{
            char time[8];
            sprintf(time, "%.1f", time_remaining);
            std::cout << "] " << "\033[1m\033[31m" << step << "\033[1m\033[32m/" << total << "\033[0m" <<  " (" << time << " s left)";
        }
        // std::cout << std::flush;
    }

    void tick(){
        double time_elapsed = difftime(time(0), start_time);
        double exp_time_remaining = time_elapsed / step * (total-step);
        show_bar_fancy(exp_time_remaining);
        step += 1;
    }
};