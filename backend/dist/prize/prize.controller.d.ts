import { PrizesService } from './prize.service';
import { Prize } from './prize.entity';
import { User } from './user.entity';
export declare class PrizesController {
    private readonly prizesService;
    constructor(prizesService: PrizesService);
    getPrize(id: number): Promise<Prize>;
    getUsers(id: number): Promise<User[]>;
    addUser(id: number, body: {
        telegram_id: number;
        username?: string;
    }): Promise<User>;
    removeUser(id: number, telegramId: number): Promise<void>;
    updatePrize(id: number, data: Partial<Prize>): Promise<Prize>;
}
