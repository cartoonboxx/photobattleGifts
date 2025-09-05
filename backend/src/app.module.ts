import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PrizesModule } from './prize/prize.module';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: '194.87.187.180',
      port: 5432,
      username: 'myuser',
      password: 'WebAppDBpass',
      database: 'webappdb',
      autoLoadEntities: true,
      synchronize: true,
    }),
    PrizesModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
