import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Prize } from './prize.entity';
import { User } from './user.entity';
import { PrizesService } from './prize.service';
import { PrizesController } from './prize.controller';

@Module({
  imports: [
    TypeOrmModule.forFeature([Prize, User]), // <-- обязательно
  ],
  providers: [PrizesService],
  controllers: [PrizesController],
  exports: [PrizesService], // если нужно использовать в других модулях
})
export class PrizesModule {}
