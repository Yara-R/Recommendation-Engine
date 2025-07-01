import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TrainingEngine } from './training-engine';

describe('TrainingEngine', () => {
  let component: TrainingEngine;
  let fixture: ComponentFixture<TrainingEngine>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TrainingEngine]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TrainingEngine);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
