import {
  Controller,
  Get,
  Param,
  Post,
  Body,
  Delete,
  Patch,
} from '@nestjs/common';
import { PrizesService } from './prize.service';
import { Prize } from './prize.entity';
import { User } from './user.entity';

@Controller('prizes')
export class PrizesController {
  constructor(private readonly prizesService: PrizesService) {}

  // 1. Получение конкурса по id
  @Get(':id')
  getPrize(@Param('id') id: number): Promise<Prize> {
    return this.prizesService.getPrizeById(id);
  }

  // 2. Получение всех пользователей конкурса
  @Get(':id/users')
  getUsers(@Param('id') id: number): Promise<User[]> {
    return this.prizesService.getUsersByPrize(id);
  }

  // 3. Добавление пользователя
  @Post(':id/users')
  addUser(
    @Param('id') id: number,
    @Body() body: { telegram_id: number; username?: string },
  ): Promise<User> {
    return this.prizesService.addUserToPrize(
      id,
      body.telegram_id,
      body.username,
    );
  }

  // 4. Удаление пользователя
  @Delete(':id/users/:telegramId')
  removeUser(@Param('id') id: number, @Param('telegramId') telegramId: number) {
    return this.prizesService.removeUserFromPrize(id, telegramId);
  }

  // 5. Обновление данных конкурса
  @Patch(':id')
  updatePrize(
    @Param('id') id: number,
    @Body() data: Partial<Prize>,
  ): Promise<Prize> {
    return this.prizesService.updatePrize(id, data);
  }
}
