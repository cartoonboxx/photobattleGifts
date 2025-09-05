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
Object.defineProperty(exports, "__esModule", { value: true });
exports.Prize = void 0;
const typeorm_1 = require("typeorm");
const user_entity_1 = require("./user.entity");
let Prize = class Prize {
    id;
    prize_size;
    channel_link;
    winners_count;
    duration_minutes;
    created;
    telegram_post_id;
    isFinished;
    channels;
    users;
};
exports.Prize = Prize;
__decorate([
    (0, typeorm_1.PrimaryGeneratedColumn)(),
    __metadata("design:type", Number)
], Prize.prototype, "id", void 0);
__decorate([
    (0, typeorm_1.Column)({ type: 'int' }),
    __metadata("design:type", Number)
], Prize.prototype, "prize_size", void 0);
__decorate([
    (0, typeorm_1.Column)({ type: 'varchar' }),
    __metadata("design:type", String)
], Prize.prototype, "channel_link", void 0);
__decorate([
    (0, typeorm_1.Column)({ type: 'int' }),
    __metadata("design:type", Number)
], Prize.prototype, "winners_count", void 0);
__decorate([
    (0, typeorm_1.Column)({ type: 'int' }),
    __metadata("design:type", Number)
], Prize.prototype, "duration_minutes", void 0);
__decorate([
    (0, typeorm_1.CreateDateColumn)(),
    __metadata("design:type", Date)
], Prize.prototype, "created", void 0);
__decorate([
    (0, typeorm_1.Column)({ type: 'int' }),
    __metadata("design:type", Number)
], Prize.prototype, "telegram_post_id", void 0);
__decorate([
    (0, typeorm_1.Column)({ type: 'boolean', default: false }),
    __metadata("design:type", Boolean)
], Prize.prototype, "isFinished", void 0);
__decorate([
    (0, typeorm_1.Column)('bigint', { array: true, default: '{}' }),
    __metadata("design:type", Array)
], Prize.prototype, "channels", void 0);
__decorate([
    (0, typeorm_1.OneToMany)(() => user_entity_1.User, (user) => user.prize, { cascade: true }),
    __metadata("design:type", Array)
], Prize.prototype, "users", void 0);
exports.Prize = Prize = __decorate([
    (0, typeorm_1.Entity)('prizes')
], Prize);
//# sourceMappingURL=prize.entity.js.map