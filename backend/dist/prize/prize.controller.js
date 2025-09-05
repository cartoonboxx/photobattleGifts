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
exports.PrizesController = void 0;
const common_1 = require("@nestjs/common");
const prize_service_1 = require("./prize.service");
let PrizesController = class PrizesController {
    prizesService;
    constructor(prizesService) {
        this.prizesService = prizesService;
    }
    getPrize(id) {
        return this.prizesService.getPrizeById(id);
    }
    getUsers(id) {
        return this.prizesService.getUsersByPrize(id);
    }
    addUser(id, body) {
        return this.prizesService.addUserToPrize(id, body.telegram_id, body.username);
    }
    removeUser(id, telegramId) {
        return this.prizesService.removeUserFromPrize(id, telegramId);
    }
    updatePrize(id, data) {
        return this.prizesService.updatePrize(id, data);
    }
};
exports.PrizesController = PrizesController;
__decorate([
    (0, common_1.Get)(':id'),
    __param(0, (0, common_1.Param)('id')),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number]),
    __metadata("design:returntype", Promise)
], PrizesController.prototype, "getPrize", null);
__decorate([
    (0, common_1.Get)(':id/users'),
    __param(0, (0, common_1.Param)('id')),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number]),
    __metadata("design:returntype", Promise)
], PrizesController.prototype, "getUsers", null);
__decorate([
    (0, common_1.Post)(':id/users'),
    __param(0, (0, common_1.Param)('id')),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Object]),
    __metadata("design:returntype", Promise)
], PrizesController.prototype, "addUser", null);
__decorate([
    (0, common_1.Delete)(':id/users/:telegramId'),
    __param(0, (0, common_1.Param)('id')),
    __param(1, (0, common_1.Param)('telegramId')),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Number]),
    __metadata("design:returntype", void 0)
], PrizesController.prototype, "removeUser", null);
__decorate([
    (0, common_1.Patch)(':id'),
    __param(0, (0, common_1.Param)('id')),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, Object]),
    __metadata("design:returntype", Promise)
], PrizesController.prototype, "updatePrize", null);
exports.PrizesController = PrizesController = __decorate([
    (0, common_1.Controller)('prizes'),
    __metadata("design:paramtypes", [prize_service_1.PrizesService])
], PrizesController);
//# sourceMappingURL=prize.controller.js.map