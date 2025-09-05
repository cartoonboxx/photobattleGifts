"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.PrizesService = void 0;
const common_1 = require("@nestjs/common");
const typeorm_1 = require("@nestjs/typeorm");
const typeorm_2 = require("typeorm");
const prize_entity_1 = require("./prize.entity");
const user_entity_1 = require("./user.entity");
let PrizesService = class PrizesService {
    prizeRepo;
    userRepo;
    constructor(prizeRepo, userRepo) {
        this.prizeRepo = prizeRepo;
        this.userRepo = userRepo;
    }
    async getPrizeById(id) {
        const prize = await this.prizeRepo.findOne({
            where: { id },
            relations: ['users'],
        });
        if (!prize)
            throw new common_1.NotFoundException('Prize not found');
        return prize;
    }
    async getUsersByPrize(id) {
        const prize = await this.getPrizeById(id);
        return prize.users;
    }
    async addUserToPrize(prizeId, telegram_id, username) {
        const prize = await this.getPrizeById(prizeId);
        let user = await this.userRepo.findOne({ where: { telegram_id } });
        if (!user) {
            user = this.userRepo.create({ telegram_id, username, prize });
        }
        else {
            user.prize = prize;
        }
        return this.userRepo.save(user);
    }
    async removeUserFromPrize(prizeId, telegram_id) {
        const user = await this.userRepo.findOne({
            where: { telegram_id },
            relations: ['prize'],
        });
        if (!user || user.prize.id !== prizeId)
            throw new common_1.NotFoundException('User not in this prize');
        await this.userRepo.remove(user);
    }
    async updatePrize(id, data) {
        await this.prizeRepo.update(id, data);
        return this.getPrizeById(id);
    }
};
exports.PrizesService = PrizesService;
exports.PrizesService = PrizesService = __decorate([
    (0, common_1.Injectable)(),
    __param(0, (0, typeorm_1.InjectRepository)(prize_entity_1.Prize)),
    __param(1, (0, typeorm_1.InjectRepository)(user_entity_1.User)),
    __metadata("design:paramtypes", [typeorm_2.Repository,
        typeorm_2.Repository])
], PrizesService);
//# sourceMappingURL=prize.service.js.map