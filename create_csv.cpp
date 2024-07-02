
#include <iostream>
#include <string>
#include <fstream>
#include <filesystem>
#include "json.hpp"

const char *fields[] = {
    "handle",
    "email",
    "vkId",
    "openId",
    "firstName",
    "lastName",
    "country",
    "city",
    "organization",
    "contribution",
    "rank",
    "rating",
    "maxRank",
    "maxRating",
    "lastOnlineTimeSeconds",
    "registrationTimeSeconds",
    "friendOfCount",
    "avatar",
    "titlePhoto"
};

int main() {

    std::ios_base::sync_with_stdio(0);
    std::cout.tie(0);

    for(size_t i = 0; i < 19; i++) {
        std::cout << fields[i];
        if(i == 18) {
            std::cout << '\n';
        } else {
            std::cout << ',';
        }
    }

    for(const auto &entry : std::filesystem::directory_iterator("./data/users")) {
        auto file = std::ifstream(entry.path());
        file.tie(0);
        auto json = nlohmann::json::parse(file);
        for(size_t i = 0; i < 19; i++) {
            auto it = json.find(fields[i]);
            if(it != json.end()) {
                std::cout << *it;
            }

            if(i == 18) {
                std::cout << '\n';
            } else {
                std::cout << ',';
            }
        }
    }

    return 0;
}
