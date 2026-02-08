#include <chrono>
#include <iostream>
#include <thread>

#if defined(_WIN32)
#include <process.h>
#define getpid _getpid
#else
#include <unistd.h>
#endif

struct Player {
    int hp = 100;
    int ammo = 30;
    int money = 999;
    float pos_x = 10.0f;
    float pos_y = 20.0f;
};

int main() {
    Player player;
    std::cout << "Demo target running. PID = " << ::getpid() << "\n";
    while (true) {
        player.hp -= 1;
        player.money += 5;
        player.pos_x += 0.1f;
        player.pos_y += 0.2f;
        std::cout << "HP=" << player.hp << " Ammo=" << player.ammo << " Money=" << player.money
                  << " Pos(" << player.pos_x << "," << player.pos_y << ")\n";
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    return 0;
}
