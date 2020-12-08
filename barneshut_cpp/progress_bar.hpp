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

    void show_bar(){
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
        std::cout << "] " << step << '/' << total;
        if (step == total) std::cout << '\n';
    }

    void show_bar_fancy(){
        double time_elapsed = difftime(time(0), start_time);
        double time_remaining = time_elapsed / step * (total-step);
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
            char formatted_seconds[8];
            int minutes = ((int) time_remaining)/60;
            float seconds = time_remaining - minutes * 60;
            int hours = minutes/60;
            minutes = minutes % 60;
            std::string time;
            if (hours != 0) time.append(std::to_string(hours)).append("h ");
            if (minutes != 0) time.append(std::to_string(minutes)).append("m ");
            sprintf(formatted_seconds, "%.1f", seconds);
            time.append(formatted_seconds).append("s ");
            std::cout << "] " << "\033[1m\033[31m" << step << "\033[1m\033[32m/" << total << "\033[0m" <<  " (" << time << "left)";
        }
        // std::cout << std::flush;
    }

    void tick(){
        show_bar_fancy();
        step += 1;
    }
};
