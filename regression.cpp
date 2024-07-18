
#include <iostream>
#include <random>
#include <vector>
#include <tuple>
#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include <chrono>

constexpr auto NUM_FEATURES = size_t(28);
constexpr auto POPULATION_SIZE = size_t(1000);
constexpr auto SURVIVE_SIZE = size_t(500);
constexpr auto NUM_GENERATIONS = size_t(100);

constexpr auto START_BASELINE = float(800);
constexpr auto START_LIMIT = float(100);
constexpr auto START_GAIN = float(0.05);
constexpr auto MIN_RATIO = float(800);

constexpr auto DEVIATION = float(1);
constexpr auto CHANGE_RATIO = float(0.01);

auto rng = std::mt19937(20042003);


std::tuple<float, std::array<float, NUM_FEATURES>> parse_line(const std::string &line) {
    auto parts = std::array<std::string, NUM_FEATURES + 2>();
    auto idx_nxt = size_t(0);
    for(auto &c : line) {
        if(c == ',') {
            idx_nxt++;
        } else {
            parts[idx_nxt].push_back(c);
        }
    }
    
    auto solved = std::array<float, NUM_FEATURES>();
    for(size_t i = 0; i < NUM_FEATURES; i++) {
        solved[i] = std::stoi(parts[i + 1]);
    }

    const auto rating = float(std::stoi(parts.back()));

    return {rating, solved};
}


struct Model {
    float baseline;
    float limit[NUM_FEATURES];
    float gain[NUM_FEATURES];
};


float evaluate(const Model &model, const std::array<float, NUM_FEATURES> &x) {
    auto result = model.baseline;
    for(size_t i = 0; i < NUM_FEATURES; i++) {
        const auto partial = model.limit[i] * (1 - std::exp(-model.gain[i] * x[i]));
        result += partial;
    }
    return result;
}

float calculate_error(const Model &model, const std::array<float, NUM_FEATURES> &x, const float y) {
    const auto diff = y - evaluate(model, x);
    return diff * diff;
}

float calculate_error_all_inputs(
    const Model &model,
    const std::vector<std::array<float, NUM_FEATURES>> &x,
    const std::vector<float> &y)
{
    auto error = float(0);
    for(size_t i = 0; i < x.size(); i++) {
        error += calculate_error(model, x[i], y[i]);
    }
    return error;
}


float mutate_value(const float value) {
    auto distribution = std::normal_distribution<float>(0, DEVIATION);
    return value * (1 + distribution(rng) * CHANGE_RATIO);
}

Model mutate(const Model &parent) {
    auto result = parent;
    result.baseline = mutate_value(result.baseline);
    for(auto &limit : result.limit) {
        limit = mutate_value(limit);
    }
    for(auto &gain : result.gain) {
        gain = mutate_value(gain);
    }
    return result;
}


Model generate_root_model() {
    Model result;
    result.baseline = START_BASELINE;
    for(auto &limit : result.limit) {
        limit = START_LIMIT;
    }
    for(auto &gain : result.gain) {
        gain = START_GAIN;
    }
    return result;
}

std::array<Model, POPULATION_SIZE> generate_first_population() {
    const auto root = generate_root_model();
    auto population = std::array<Model, POPULATION_SIZE>();
    for(auto &model : population) {
        model = mutate(root);
    }
    return population;
}


int main() {

    auto line = std::string();
    std::cin >> line;

    auto y = std::vector<float>();
    auto x = std::vector<std::array<float, NUM_FEATURES>>();
    while(std::cin >> line) {
        const auto [cy, cx] = parse_line(line);
        if(cy < MIN_RATIO) {
            continue;
        }
        y.push_back(cy);
        x.push_back(cx);
    }

    auto population1 = std::array<Model, POPULATION_SIZE>();
    auto population2 = std::array<Model, POPULATION_SIZE>();

    auto *cur_population = &population1;
    auto *nxt_population = &population2;
    *cur_population = generate_first_population();

    for(size_t i = 0; i < NUM_GENERATIONS; i++) {
        std::array<std::pair<float, uint32_t>, POPULATION_SIZE> evaluation;
        for(size_t j = 0; j < POPULATION_SIZE; j++) {
            evaluation[j] = {calculate_error_all_inputs((*cur_population)[j], x, y), uint32_t(j)};
        }

        std::sort(evaluation.begin(), evaluation.end());
        std::cout << evaluation[0].first << '\n';
        std::cout << (*cur_population)[evaluation[0].second].baseline << '\n';
        for(auto &limit : (*cur_population)[evaluation[0].second].limit) {
            std::cout << limit << ' ';
        }
        std::cout << '\n';
        for(auto &gain : (*cur_population)[evaluation[0].second].gain) {
            std::cout << gain << ' ';
        }
        std::cout << '\n';

        for(size_t j = 0; j < SURVIVE_SIZE; j++) {
            (*nxt_population)[j] = (*cur_population)[evaluation[j].second];
        }
        for(size_t j = SURVIVE_SIZE; j < POPULATION_SIZE; j++) {
            (*nxt_population)[j] = mutate((*cur_population)[evaluation[j - SURVIVE_SIZE].second]);
        }

        std::swap(cur_population, nxt_population);
    }

    return 0;
}
