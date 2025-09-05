import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Prize } from './prize.entity';
import { User } from './user.entity';

@Injectable()
export class PrizesService {
  constructor(
    @InjectRepository(Prize) private prizeRepo: Repository<Prize>,
    @InjectRepository(User) private userRepo: Repository<User>,
  ) {}

  async getPrizeById(id: number): Promise<Prize> {
    const prize = await this.prizeRepo.findOne({
      where: { id },
      relations: ['users'],
    });
    if (!prize) throw new NotFoundException('Prize not found');
    return prize;
  }

  async getUsersByPrize(id: number): Promise<User[]> {
    const prize = await this.getPrizeById(id);
    return prize.users;
  }

  async addUserToPrize(
    prizeId: number,
    telegram_id: number,
    username?: string,
  ): Promise<User> {
    const prize = await this.getPrizeById(prizeId);

    let user = await this.userRepo.findOne({ where: { telegram_id } });
    if (!user) {
      user = this.userRepo.create({ telegram_id, username, prize });
    } else {
      user.prize = prize;
    }
    return this.userRepo.save(user);
  }

  async removeUserFromPrize(
    prizeId: number,
    telegram_id: number,
  ): Promise<void> {
    const user = await this.userRepo.findOne({
      where: { telegram_id },
      relations: ['prize'],
    });
    if (!user || user.prize.id !== prizeId)
      throw new NotFoundException('User not in this prize');
    await this.userRepo.remove(user);
  }

  async updatePrize(id: number, data: Partial<Prize>): Promise<Prize> {
    await this.prizeRepo.update(id, data);
    return this.getPrizeById(id);
  }
}
