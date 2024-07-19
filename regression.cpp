
#include <iostream>
#include <random>
#include <vector>
#include <tuple>
#include <vector>
#include <array>
#include <cmath>
#include <algorithm>
#include <chrono>
#include <future>

constexpr auto NUM_THREADS = size_t(12);

constexpr auto NUM_FEATURES = size_t(28);
constexpr auto POPULATION_SIZE = size_t(1200);
constexpr auto SURVIVE_SIZE = size_t(120);
constexpr auto NUM_GENERATIONS = size_t(5000);

constexpr auto START_BASELINE = float(700);
constexpr auto START_LIMIT = float(100);
constexpr auto START_GAIN = float(0.05);
constexpr auto MIN_RATIO = float(700);
constexpr auto MIN_PROBLEMS_SOLVED = float(20);

constexpr auto START_CHANGE_RATIO = float(0.00001);
constexpr auto END_CHANGE_RATIO = float(0.1);

auto rng = std::mt19937(30062003);


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


float mutate_value(const float value, const float change_ratio) {
    auto distribution = std::normal_distribution<float>();
    while(true) {
        const auto res = value * (1 + distribution(rng) * change_ratio);
        if(res > 0) {
            return res;
        }
    }
}

Model mutate(const Model &parent, const float change_ratio) {
    auto result = parent;
    result.baseline = mutate_value(result.baseline, change_ratio);
    for(auto &limit : result.limit) {
        limit = mutate_value(limit, change_ratio);
    }
    for(auto &gain : result.gain) {
        gain = mutate_value(gain, change_ratio);
    }
    return result;
}

Model join(const Model &parent1, const Model &parent2) {
    auto result = Model();
    result.baseline = (parent1.baseline + parent2.baseline) / 2;
    for(size_t i = 0; i < NUM_FEATURES; i++) {
        result.limit[i] = (parent1.limit[i] + parent2.limit[i]) / 2;
        result.gain[i] = (parent1.gain[i] + parent2.gain[i]) / 2;
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
        model = mutate(root, END_CHANGE_RATIO);
    }
    return population;
}

// Range in interval [l, r]
size_t gen_range(const size_t l, const size_t r) {
    auto distribution = std::uniform_int_distribution<size_t>(l, r);
    return distribution(rng);
}

float sum_problems(const std::array<float, NUM_FEATURES> &x) {
    float sum = 0;
    for(auto &t : x) {
        sum += t;
    }
    return sum;
}

int main() {

    auto line = std::string();
    std::cin >> line;

    auto y = std::vector<float>();
    auto x = std::vector<std::array<float, NUM_FEATURES>>();
    while(std::cin >> line) {
        const auto [cy, cx] = parse_line(line);
        const auto sum = sum_problems(cx);
        if(cy < MIN_RATIO || sum < MIN_PROBLEMS_SOLVED) {
            continue;
        }
        y.push_back(cy);
        x.push_back(cx);
    }
    // Numero de linhas: 48323


    auto population1 = std::array<Model, POPULATION_SIZE>();
    auto population2 = std::array<Model, POPULATION_SIZE>();

    auto *cur_population = &population1;
    auto *nxt_population = &population2;
    *cur_population = generate_first_population();

    for(size_t i = 0; i < NUM_GENERATIONS; i++) {
        std::array<std::pair<float, uint32_t>, POPULATION_SIZE> evaluation;

        constexpr auto MODELS_PER_THREAD = POPULATION_SIZE / NUM_THREADS;
        auto futures = std::vector<std::future<void>>();
        for(size_t j = 0; j < POPULATION_SIZE; j += MODELS_PER_THREAD) {
            futures.push_back(std::async(std::launch::async, [j, &evaluation, cur_population, &x, &y]() {
                for(size_t k = j; k < j + MODELS_PER_THREAD; k++) {
                    evaluation[k] = {calculate_error_all_inputs((*cur_population)[k], x, y), uint32_t(k)};
                }
            }));
        }
        
        for(auto &future : futures) {
            future.wait();
        }

        std::sort(evaluation.begin(), evaluation.end());

        std::cout << i << '/' << NUM_GENERATIONS << '\n';
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

        const auto grow_ratio = END_CHANGE_RATIO / START_CHANGE_RATIO;
        const auto grow_step = std::pow(grow_ratio, 1.0f / (POPULATION_SIZE - SURVIVE_SIZE));
        for(size_t j = 0; j < SURVIVE_SIZE; j++) {
            (*nxt_population)[j] = (*cur_population)[evaluation[j].second];
        }
        for(size_t j = SURVIVE_SIZE; j < POPULATION_SIZE; j++) {
            const auto idx1 = gen_range(0, SURVIVE_SIZE - 1);
            const auto idx2 = gen_range(0, SURVIVE_SIZE - 1);
            const auto &parent1 = (*cur_population)[idx1];
            const auto &parent2 = (*cur_population)[idx2];
            const auto change_ratio = START_CHANGE_RATIO * std::pow(grow_step, float(j - SURVIVE_SIZE));
            (*nxt_population)[j] = mutate(join(parent1, parent2), change_ratio);
        }

        std::swap(cur_population, nxt_population);
    }

    return 0;
}
