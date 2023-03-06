#include <math.h>  // for fabs()
#include <float.h> // for DBL_MIN
#include "config.h"
#include "model.h"

#define V_MIN (0.1)
#define EVENT_EPSILON (1e-10)


void setStartValues(ModelInstance *comp) {
    M(u)         =  0;
    M(y)         =  0;
    M(r)         =  0;
    M(e_ls)		 =  0;
    M(I_ls) 	 =  0;
    M(kp)        =  0;
    M(ki)        =  0;
    M(kd)        =  0;
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
