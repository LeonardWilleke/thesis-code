#ifndef config_h
#define config_h

// define class name and unique id
#define MODEL_IDENTIFIER PIDcontroller
#define INSTANTIATION_TOKEN "{1AE5E10D-9521-4DE3-80B9-D0EAAA7D5AF1}"

#define CO_SIMULATION
#define MODEL_EXCHANGE

// define model size
#define NX 2
#define NZ 1

#define SET_FLOAT64
#define GET_OUTPUT_DERIVATIVE
#define EVENT_UPDATE

#define FIXED_SOLVER_STEP 1e-3
#define DEFAULT_STOP_TIME 3

typedef enum {
    vr_time, vr_u, vr_y, vr_r, vr_e, vr_e_ls, vr_I_ls, vr_kp, vr_ki, vr_kd
} ValueReference;

typedef struct {

    double u;
    double y;
    double r;
    double e;
    double e_ls;
    double I_ls;
    double kp;
    double ki;
    double kd;

} ModelData;

#endif /* config_h */
