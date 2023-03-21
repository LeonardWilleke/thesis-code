#include <math.h>  // for fabs()
#include <float.h> // for DBL_MIN
#include "config.h"
#include "model.h"

#define V_MIN (0.1)
#define EVENT_EPSILON (1e-10)


void setStartValues(ModelInstance *comp) {
    //M(u)        = 0;
    //M(y)        = 0;
    M(u)[0][0]		= 0;
    M(y)[0][0]		= 0;
    //M(y)		= {	{0.0, 0.1},
	//				{1.0, 1.1},
    //               	{2.0, 2.1},
    //               	{3.0, 3.1},
    //               	{4.0, 4.1},
    //               	{5.0, 5.1},
    //               	{6.0, 6.1},
    //               	{7.0, 7.1},
    //               	{8.0, 8.1},
    //               	{9.0, 9.1},
    //               	{10.0, 10.1},
    //               	{11.0, 11.1},
    //               	{12.0, 12.1},
    //               	{13.0, 13.1},
    //               	{14.0, 14.1},
    //               	{15.0, 15.1},
    //               	{16.0, 16.1}};
    M(r)        = 0;
    M(e_ls)		= 0;
    M(kp)       = 0;
    M(ki)       = 0;
    M(kd)       = 0;
    M(P)		= 0;
    M(I)		= 0;
    M(D)		= 0;
    
}

Status calculateValues(ModelInstance *comp) {
    
    UNUSED(comp);
    return OK;
    
}

Status getFloat64(ModelInstance* comp, ValueReference vr, double *value, size_t *index) {
    switch (vr) {
        case vr_time:
            value[(*index)++] = comp->time;
            return OK;
        case vr_u:
            value[(*index)++] = M(u);
            return OK;
        case vr_y:
            value[(*index)++] = M(y);
            return OK;
        case vr_r:
            value[(*index)++] = M(r);
            return OK;
        case vr_e:
            value[(*index)++] = M(e);
            return OK;
        case vr_e_ls:
            value[(*index)++] = M(e_ls);
            return OK;
        case vr_kp:
            value[(*index)++] = M(kp);
            return OK;
        case vr_ki:
            value[(*index)++] = M(ki);
            return OK;
        case vr_kd:
            value[(*index)++] = M(kd);
            return OK;
        case vr_P:
            value[(*index)++] = M(P);
            return OK;
        case vr_I:
            value[(*index)++] = M(I);
            return OK;
        case vr_D:
            value[(*index)++] = M(D);
            return OK;
        default:
            logError(comp, "Get Float64 is not allowed for value reference %u.", vr);
            return Error;
    }
}

Status setFloat64(ModelInstance* comp, ValueReference vr, const double *value, size_t *index) {
    switch (vr) {

        case vr_u:
            M(u) = value[(*index)++];
            return OK;
        case vr_y:
            M(y) = value[(*index)++];
            return OK;
        case vr_r:
            M(r) = value[(*index)++];
            return OK;
        case vr_kp:
            M(kp) = value[(*index)++];
            return OK;
        case vr_ki:
            M(ki) = value[(*index)++];
            return OK;
        case vr_kd:
            M(kd) = value[(*index)++];
            return OK;
        default:
            logError(comp, "Unexpected value reference: %u.", vr);
            return Error;
    }
}

Status getOutputDerivative(ModelInstance *comp, ValueReference valueReference, int order, double *value) {

    if (order != 1) {
        logError(comp, "The output derivative order %d for value reference %u is not available.", order, valueReference);
        return Error;
    }

    switch (valueReference) {

    default:
        logError(comp, "The output derivative for value reference %u is not available.", valueReference);
        return Error;
    }
    
    UNUSED(value);
}

void eventUpdate(ModelInstance *comp) {

    if (false) {
    
    } else {
        comp->valuesOfContinuousStatesChanged = false;
    }

    comp->nominalsOfContinuousStatesChanged = false;
    comp->terminateSimulation  = false;
    comp->nextEventTimeDefined = false;
}

void getContinuousStates(ModelInstance *comp, double x[], size_t nx) {
    UNUSED(comp);
    UNUSED(nx);
    UNUSED(x);
}

void setContinuousStates(ModelInstance *comp, const double x[], size_t nx) {
    UNUSED(comp);
    UNUSED(nx);
    UNUSED(x);
}

void getDerivatives(ModelInstance *comp, double dx[], size_t nx) {
    UNUSED(comp);
    UNUSED(nx);
    UNUSED(dx);
}

void getEventIndicators(ModelInstance *comp, double z[], size_t nz) {

    UNUSED(nz);
    UNUSED(comp);
    UNUSED(z);

}
